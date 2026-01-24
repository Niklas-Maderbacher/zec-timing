import { jwtDecode } from 'jwt-decode';

interface TokenData {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  refresh_expires_in: number;
  token_type: string;
}

interface DecodedToken {
  exp: number;
  iat: number;
  sub: string;
  preferred_username: string;
  realm_access?: {
    roles: string[];
  };
  resource_access?: {
    [key: string]: {
      roles: string[];
    };
  };
}

const API_BASE_URL = typeof window !== 'undefined' 
  ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost')
  : 'http://localhost';

export class AuthService {
  private static ACCESS_TOKEN_KEY = 'access_token';
  private static REFRESH_TOKEN_KEY = 'refresh_token';
  private static TOKEN_EXPIRY_KEY = 'token_expiry';

  static async login(username: string, password: string): Promise<TokenData> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        body: formData,
        mode: 'cors',
        credentials: 'include',
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Login failed' }));
        throw new Error(error.detail || 'Login failed');
      }

      const tokenData: TokenData = await response.json();
      this.saveTokens(tokenData);
      return tokenData;
    } catch (error) {
      console.error('Login error:', error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Cannot connect to server. Please check if the API is running.');
      }
      throw error;
    }
  }

  static async refresh(): Promise<TokenData> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const formData = new FormData();
    formData.append('refresh_token', refreshToken);

    try {
      const response = await fetch(`${API_BASE_URL}/refresh`, {
        method: 'POST',
        body: formData,
        mode: 'cors',
        credentials: 'include',
      });

      if (!response.ok) {
        this.clearTokens();
        throw new Error('Token refresh failed');
      }

      const tokenData: TokenData = await response.json();
      this.saveTokens(tokenData);
      return tokenData;
    } catch (error) {
      this.clearTokens();
      throw error;
    }
  }

  static saveTokens(tokenData: TokenData): void {
    localStorage.setItem(this.ACCESS_TOKEN_KEY, tokenData.access_token);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, tokenData.refresh_token);
    
    const expiryTime = Date.now() + tokenData.expires_in * 1000;
    localStorage.setItem(this.TOKEN_EXPIRY_KEY, expiryTime.toString());
  }

  static getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }

  static getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  static clearTokens(): void {
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.TOKEN_EXPIRY_KEY);
  }

  static isTokenExpired(): boolean {
    const expiry = localStorage.getItem(this.TOKEN_EXPIRY_KEY);
    if (!expiry) return true;
    return Date.now() >= parseInt(expiry);
  }

  static async getValidToken(): Promise<string | null> {
    if (!this.isTokenExpired()) {
      return this.getAccessToken();
    }

    try {
      await this.refresh();
      return this.getAccessToken();
    } catch (error) {
      this.clearTokens();
      return null;
    }
  }

  static decodeToken(token: string): DecodedToken | null {
    try {
      return jwtDecode<DecodedToken>(token);
    } catch (error) {
      console.error('Failed to decode token:', error);
      return null;
    }
  }

  static getUserRole(token?: string): string | null {
    const accessToken = token || this.getAccessToken();
    if (!accessToken) return null;

    const decoded = this.decodeToken(accessToken);
    if (!decoded) return null;

    if (decoded.resource_access) {
      for (const resource of Object.values(decoded.resource_access)) {
        if (resource.roles && resource.roles.length > 0) {
          const commonRoles = ['admin', 'team_lead', 'viewer'];
          const foundRole = resource.roles.find(role => 
            commonRoles.includes(role.toLowerCase())
          );
          if (foundRole) return foundRole.toLowerCase();
          return resource.roles[0]?.toLowerCase();
        }
      }
    }
    return null;
  }

  static getUsername(token?: string): string | null {
    const accessToken = token || this.getAccessToken();
    if (!accessToken) return null;

    const decoded = this.decodeToken(accessToken);
    return decoded?.preferred_username || decoded?.sub || null;
  }

  static isLoggedIn(): boolean {
    return !!this.getAccessToken() && !this.isTokenExpired();
  }
}

export async function authenticatedFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = await AuthService.getValidToken();
  
  if (!token) {
    throw new Error('Not authenticated');
  }
  console.log('🔍 Debug Info:', {
    url,
    hasToken: !!token,
    tokenPreview: token?.substring(0, 20) + '...',
    isExpired: AuthService.isTokenExpired()
  });

  const headers = new Headers(options.headers);
  headers.set('Authorization', `Bearer ${token}`);
  if (!(options.body instanceof FormData)) {
    if (!headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json');
    }
  }

  return fetch(url, {
    ...options,
    headers,
  });
}