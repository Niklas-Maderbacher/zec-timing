'use client'

import axios from "axios";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuRadioItem,
  DropdownMenuRadioGroup,
} from "@/components/ui/dropdown-menu";

import { API_URL } from "@/next.config";

interface Team {
  id: number;
  name: string;
}

interface Challenge {
  id: number;
  name: string;
  esp_mac_start1: string;
  esp_mac_start2: string;
  esp_mac_finish1: string;
  esp_mac_finish2: string;
}

interface Pentalty {
  id: number
  amount: number;
  type: String | null;
}

interface ConnectionStatus {
  is_active: boolean;
}

export default function Page() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);

  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);

  const [espStart1Input, setEspStart1Input] = useState("");
  const [espStart2Input, setEspStart2Input] = useState("");
  const [espFinish1Input, setEspFinish1Input] = useState("");
  const [espFinish2Input, setEspFinish2Input] = useState("");

  const [penalties, setPenalties] = useState<Pentalty[]>([]);
  const [selectedPenalty, setSelectedPenalty] = useState<Pentalty | null>(null);

  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    is_active: false,
  });


  // Fetch Teams
  const fetchTeams = async () => {
    try {
      const response = await axios.get(`${API_URL}/teams/`);
      setTeams(response.data);

      if (response.data.length > 0) {
        setSelectedTeam(response.data[0]); // default first team
      }
    } catch (error) {
      console.error("Failed to fetch teams", error);
    }
  };

  // Fetch Challenges
  const fetchChallenges = async () => {
    try {
      const response = await axios.get(`${API_URL}/challenges/`);
      setChallenges(response.data);

      if (response.data.length > 0) {
        setSelectedChallenge(response.data[0]); // default first challenge
      }
    } catch (error) {
      console.error("Failed to fetch challenges", error);
    }
  };

  const fetchPenalties = async () => {
    try {
      const response = await axios.get(`${API_URL}/penalties/`);
      setPenalties(response.data);

      if (response.data.length > 0) {
        setSelectedPenalty(response.data[0]);
      }
    } catch (error) {
      console.error("Failed to fetch penalties", error);
    }
  }

  // Fetch both on mount
  useEffect(() => {
    fetchTeams();
    fetchChallenges();
    fetchPenalties();
  }, []);

  return (
    <div className="p-6">
      <header className="flex items-center justify-between mb-8">
        <div className="flex items-center">
          <img src="images/Logo_HTL_100.png" className="h-30" />
        </div>
        <h1 className="text-2xl md:text-6xl font-bold tracking-tight text-blue-900">
          Zero Emission Challenge Timing
        </h1>
        <div className="flex items-center">
          <img src="images/ZEC-Logo.png" className="h-30" />
        </div>
      </header>

      <div className="flex justify-between">
        {/* Challenge Penalty */}
        <div className="mb-6">
          {/* Challenge */}
          <div className="justify-center">
            <h2 className="text-2xl md:text-4xl font-bold tracking-tight text-black mb-2 justify-center">
              Challenge
            </h2>
            <div className="flex justify-center">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline">
                    {selectedChallenge ? selectedChallenge.name : "Select Challenge"}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuRadioGroup
                    value={selectedChallenge?.id.toString() || ""}
                    onValueChange={(value) => {
                      const challenge = challenges.find((c) => c.id.toString() === value) || null;
                      setSelectedChallenge(challenge);
                    }}
                  >
                    {challenges.map((challenge) => (
                      <DropdownMenuRadioItem
                        key={challenge.id}
                        value={challenge.id.toString()}
                      >
                        {challenge.name}
                      </DropdownMenuRadioItem>
                    ))}
                  </DropdownMenuRadioGroup>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
          {/* Penalty */}
          <div className="">
            <h2 className="text-2xl md:text-4xl font-bold tracking-tight text-black mb-2 justify-center">
              Time Penalty
            </h2>
            <div className="flex justify-center">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline">
                    {selectedPenalty ? selectedPenalty.type : "Select Penalty"}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuRadioGroup
                    value={selectedPenalty?.id.toString() || ""}
                    onValueChange={(value) => {
                      const penalty = penalties.find((p) => p.id.toString() === value) || null;
                      setSelectedPenalty(penalty);
                    }}
                  >
                    {penalties.map((penalty) => (
                      <DropdownMenuRadioItem key={penalty.id} value={penalty.id.toString()}>
                        {penalty.type}
                      </DropdownMenuRadioItem>
                    ))}
                  </DropdownMenuRadioGroup>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>

        <div className="mb-6">
          {/* Team Selection */}
          <div>
            <h2 className="text-2xl md:text-4xl font-bold tracking-tight text-black mb-2 justify-center">
              Team
            </h2>
            <div className="flex justify-center">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline">
                    {selectedTeam ? selectedTeam.name : "Select Team"}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuRadioGroup
                    value={selectedTeam?.id.toString() || ""}
                    onValueChange={(value) => {
                      const team = teams.find((t) => t.id.toString() === value) || null;
                      setSelectedTeam(team);
                    }}
                  >
                    {teams.map((team) => (
                      <DropdownMenuRadioItem key={team.id} value={team.id.toString()}>
                        {team.name}
                      </DropdownMenuRadioItem>
                    ))}
                  </DropdownMenuRadioGroup>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>

          {/* Status */}
          <div className="flex flex-col gap-6">

            {/* Status Row */}
            <div className="flex items-center gap-4">
              <p className="text-3xl font-semibold">Status:</p>
              <p
                className={`text-3xl font-bold ${connectionStatus.is_active ? "text-green-600" : "text-red-600"
                  }`}
              >
                {connectionStatus.is_active ? "ACTIVE" : "INACTIVE"}
              </p>
            </div>

            {/* Buttons Row */}
            <div className="flex gap-6">
              <Button
                onClick={() => setConnectionStatus({ is_active: true })}
                className="bg-green-600 hover:bg-green-700 text-white text-2xl px-6 py-3"
              >
                Activate
              </Button>

              <Button
                onClick={() => setConnectionStatus({ is_active: false })}
                className="bg-red-600 hover:bg-red-700 text-white text-2xl px-6 py-3"
              >
                Deactivate
              </Button>
            </div>
          </div>
        </div>

        {/*Pairing*/}
        <div className="mb-6">
          <h2 className="text-2xl md:text-4xl font-bold tracking-tight text-black mb-2">
            Pairing
          </h2>
          <div>
            {/*Start 1*/}
            <div className="flex items-center gap-2 mt-4">
              <Input
                value={espStart1Input}
                onChange={(e) => setEspStart1Input(e.target.value)}
                placeholder={selectedChallenge?.esp_mac_start1}
              />
              <Button
                onClick={() => {
                  if (selectedChallenge) {
                    setSelectedChallenge({
                      ...selectedChallenge,
                      esp_mac_start1: espStart1Input, // update the property
                    });
                    setEspStart1Input(""); // optionally clear the input
                  }
                }}
              >
                Update Start 1
              </Button>
            </div>
            {/*Start 2*/}
            <div className="flex items-center gap-2 mt-4">
              <Input
                value={espStart2Input}
                onChange={(e) => setEspStart2Input(e.target.value)}
                placeholder={selectedChallenge?.esp_mac_start2}
              />
              <Button
                onClick={() => {
                  if (selectedChallenge) {
                    setSelectedChallenge({
                      ...selectedChallenge,
                      esp_mac_start2: espStart2Input, // update the property
                    });
                    setEspStart2Input(""); // optionally clear the input
                  }
                }}
              >
                Update Start 2
              </Button>
            </div>
            {/*Finish 1*/}
            <div className="flex items-center gap-2 mt-4">
              <Input
                value={espFinish1Input}
                onChange={(e) => setEspFinish1Input(e.target.value)}
                placeholder={selectedChallenge?.esp_mac_finish1}
              />
              <Button
                onClick={() => {
                  if (selectedChallenge) {
                    setSelectedChallenge({
                      ...selectedChallenge,
                      esp_mac_finish1: espFinish1Input, // update the property
                    });
                    setEspFinish1Input(""); // optionally clear the input
                  }
                }}
              >
                Update Finish 1
              </Button>
            </div>
            {/*Finish 2*/}
            <div className="flex items-center gap-2 mt-4">
              <Input
                value={espFinish2Input}
                onChange={(e) => setEspFinish2Input(e.target.value)}
                placeholder={selectedChallenge?.esp_mac_finish2}
              />
              <Button
                onClick={() => {
                  if (selectedChallenge) {
                    setSelectedChallenge({
                      ...selectedChallenge,
                      esp_mac_finish2: espFinish2Input, // update the property
                    });
                    setEspFinish2Input(""); // optionally clear the input
                  }
                }}
              >
                Update Finish 2
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div >
  );
}
