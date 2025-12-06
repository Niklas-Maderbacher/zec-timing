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

export default function Page() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);

  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);

  const [espStart1Input, setEspStart1Input] = useState("");
  const [espStart2Input, setEspStart2Input] = useState("");
  const [espFinish1Input, setEspFinish1Input] = useState("");
  const [espFinish2Input, setEspFinish2Input] = useState("");


  // Fetch Teams
  const fetchTeams = async () => {
    try {
      const response = await axios.get("http://localhost:8002/api/teams/");
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
      const response = await axios.get("http://localhost:8002/api/challenges/");
      setChallenges(response.data);

      if (response.data.length > 0) {
        setSelectedChallenge(response.data[0]); // default first challenge
      }
    } catch (error) {
      console.error("Failed to fetch challenges", error);
    }
  };

  // Fetch both on mount
  useEffect(() => {
    fetchTeams();
    fetchChallenges();
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

      {/* Challenge Selection */}
      <div className="flex justify-between">
        <div className="mb-6">
          <h2 className="text-2xl md:text-4xl font-bold tracking-tight text-black mb-2">
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

        {/* Team Selection */}
        <div className="mb-6">
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
    </div>
  );
}
