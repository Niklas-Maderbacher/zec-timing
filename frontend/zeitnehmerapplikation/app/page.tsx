'use client'

import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useEffect, useState } from "react";

import { SERVER_API_URL, MQTT_WORKER_API_URL, API_KEY } from "@/lib/env";
import { FormulaCard } from "@/components/FormulaCard";
import { SelectionCard } from "@/components/SelectionCard";
import { MacInputRow } from "@/components/MacInputRow";
import { ZECHeader } from "@/components/ZECHeader";
import { NumberInputCard } from "@/components/NumberInputCard";
import { ConnectionStatusCard } from "@/components/ConnectionStatusCard";
import { TimestampSelector } from "@/components/TimestampSelector";
import { AttemptResultCard } from "@/components/AttemptResultCard";
import { Team, Challenge, Penalty, ConnectionStatus, Driver } from "@/components/types"
import { medianTimestamp } from "@/components/medianTimestamp";

export default function Page() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);

  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);

  const [espStart1Input, setEspStart1Input] = useState("");
  const [espStart2Input, setEspStart2Input] = useState("");
  const [espFinish1Input, setEspFinish1Input] = useState("");
  const [espFinish2Input, setEspFinish2Input] = useState("");
  const [manualAttemptTime, setManualAttemptTime] = useState<string | null>(null);

  const [penalties, setPenalties] = useState<Penalty[]>([]);
  const [selectedPenalty, setSelectedPenalty] = useState<Penalty | null>(null);

  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    is_active: false,
  });

  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [selectedDriver, setSelectedDriver] = useState<Driver | null>(null);

  const [penaltyCount, SetPenaltyCount] = useState<number>(0);
  const [energyConsumption, setEnergyConsumption] = useState<number>(0.0);

  const [startTimestamps, setStartTimestamps] = useState<string[]>([]);
  const [endTimestamps, setEndTimestamps] = useState<string[]>([]);

  const [selectedStartTimestamps, setSelectedStartTimestamps] = useState<string[] | null>(null);
  const [selectedEndTimestamps, setSelectedEndTimestamps] = useState<string[] | null>(null);

  // Compute median timestamps as strings
  const medianStartTimestamp = medianTimestamp(selectedStartTimestamps ?? []);
  const medianEndTimestamp = medianTimestamp(selectedEndTimestamps ?? []);

  // Reset function to clear all dynamic state
  const resetForm = () => {
    // Clear timestamps
    setStartTimestamps([]);
    setEndTimestamps([]);
    setSelectedStartTimestamps(null);
    setSelectedEndTimestamps(null);

    // Clear manual inputs
    setManualAttemptTime(null);
    setEspStart1Input("");
    setEspStart2Input("");
    setEspFinish1Input("");
    setEspFinish2Input("");

    // Clear numbers
    SetPenaltyCount(0);
    setEnergyConsumption(0.0);

    // Reset selections to first items
    if (teams.length > 0) setSelectedTeam(teams[0]);
    if (challenges.length > 0) setSelectedChallenge(challenges[0]);
    if (penalties.length > 0) setSelectedPenalty(penalties[0]);
    if (drivers.length > 0) setSelectedDriver(drivers[0]);
  };

  // Fetch Teams
  const fetchTeams = async () => {
    try {
      const response = await axios.get<Team[]>(
        `${SERVER_API_URL}/teams/`,
        {
          headers: {
            "x-api-key": API_KEY
          }
        }
      );

      setTeams(response.data);
      if (response.data.length > 0) setSelectedTeam(response.data[0]);
    } catch (error) {
      console.error("Failed to fetch teams", error);
    }
  };

  // Fetch Challenges
  const fetchChallenges = async () => {
    try {
      const response = await axios.get<Challenge[]>(
        `${SERVER_API_URL}/challenges/`
      );
      setChallenges(response.data);
      if (response.data.length > 0) setSelectedChallenge(response.data[0]);
    } catch (error) {
      console.error("Failed to fetch challenges", error);
    }
  };

  // Fetch Penalties
  const fetchPenalties = async () => {
    try {
      const response = await axios.get<Penalty[]>(
        `${SERVER_API_URL}/penalties/types/`,
        {
          headers: {
            "x-api-key": API_KEY
          }
        }
      );
      setPenalties(response.data);
      if (response.data.length > 0) setSelectedPenalty(response.data[0]);
    } catch (error) {
      console.error("Failed to fetch penalties", error);
    }
  };

  // Fetch Drivers for selected team
  const fetchDriversForTeam = async (teamId: number | undefined) => {
    if (!teamId) return;
    try {
      const response = await axios.get<Driver[]>(
        `${SERVER_API_URL}/drivers/team/${teamId}`,
        {
          headers: {
            "x-api-key": API_KEY
          }
        }
      );
      setDrivers(response.data);
      if (response.data.length > 0) setSelectedDriver(response.data[0]);
    } catch (error) {
      console.error("Failed to fetch drivers", error);
    }
  };

  // Fetch timestamps
  const fetchStartTimestamps = async () => {
    if (!selectedChallenge) return;
    try {
      const start_1 = await axios.get<{ timestamp: string[] }>(`${MQTT_WORKER_API_URL}/timestamps/${selectedChallenge.esp_mac_start1.replace(/:/g, '-')}`);
      const start_2 = await axios.get<{ timestamp: string[] }>(`${MQTT_WORKER_API_URL}/timestamps/${selectedChallenge.esp_mac_start2.replace(/:/g, '-')}`);
      const combined = [...(start_1.data.timestamp || []), ...(start_2.data.timestamp || [])];
      setStartTimestamps(combined);
    } catch (error) {
      console.error("Failed to fetch start timestamps", error);
    }
  };

  const fetchEndTimestamps = async () => {
    if (!selectedChallenge) return;
    try {
      const end_1 = await axios.get<{ timestamp: string[] }>(`${MQTT_WORKER_API_URL}/timestamps/${selectedChallenge.esp_mac_finish1.replace(/:/g, '-')}`);
      const end_2 = await axios.get<{ timestamp: string[] }>(`${MQTT_WORKER_API_URL}/timestamps/${selectedChallenge.esp_mac_finish2.replace(/:/g, '-')}`); 3
      const combined = [...(end_1.data.timestamp || []), ...(end_2.data.timestamp || [])];
      setEndTimestamps(combined);
    } catch (error) {
      console.error("Failed to fetch end timestamps", error);
    }
  };

  // Fetch on mount
  useEffect(() => {
    fetchTeams();
    fetchChallenges();
    fetchPenalties();
  }, []);

  useEffect(() => {
    if (!selectedTeam) return;
    fetchDriversForTeam(selectedTeam.id);
  }, [selectedTeam]);

  useEffect(() => {
    if (!connectionStatus.is_active) return;

    fetchStartTimestamps();
    fetchEndTimestamps();

    const interval = setInterval(() => {
      fetchStartTimestamps();
      fetchEndTimestamps();
    }, 3000);

    return () => clearInterval(interval);
  }, [connectionStatus.is_active, selectedChallenge]);

  return (
    <div>
      <ZECHeader />

      <div className="grid grid-cols-1 md:grid-cols-3 mb-4 gap-6">
        {/* Challenge */}
        <SelectionCard<Challenge>
          title="Challenge"
          items={challenges}
          selectedItem={selectedChallenge}
          onSelect={setSelectedChallenge}
        />

        {/* Team */}
        <SelectionCard<Team>
          title="Team"
          items={teams}
          selectedItem={selectedTeam}
          onSelect={(team) => {
            setSelectedTeam(team)
            fetchDriversForTeam(team?.id)
          }}
        />

        <Card className="md:row-span-2">
          <CardHeader>
            <CardTitle>Pairing</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <MacInputRow
              label="Update Start 1"
              value={espStart1Input}
              placeholder={selectedChallenge?.esp_mac_start1}
              onChange={setEspStart1Input}
              onUpdate={() => {
                if (selectedChallenge) {
                  setSelectedChallenge({ ...selectedChallenge, esp_mac_start1: espStart1Input })
                  setEspStart1Input("")
                }
              }}
            />

            <MacInputRow
              label="Update Start 2"
              value={espStart2Input}
              placeholder={selectedChallenge?.esp_mac_start2}
              onChange={setEspStart2Input}
              onUpdate={() => {
                if (selectedChallenge) {
                  setSelectedChallenge({ ...selectedChallenge, esp_mac_start2: espStart2Input })
                  setEspStart2Input("")
                }
              }}
            />

            <MacInputRow
              label="Update Finish 1"
              value={espFinish1Input}
              placeholder={selectedChallenge?.esp_mac_finish1}
              onChange={setEspFinish1Input}
              onUpdate={() => {
                if (selectedChallenge) {
                  setSelectedChallenge({ ...selectedChallenge, esp_mac_finish1: espFinish1Input })
                  setEspFinish1Input("")
                }
              }}
            />

            <MacInputRow
              label="Update Finish 2"
              value={espFinish2Input}
              placeholder={selectedChallenge?.esp_mac_finish2}
              onChange={setEspFinish2Input}
              onUpdate={() => {
                if (selectedChallenge) {
                  setSelectedChallenge({ ...selectedChallenge, esp_mac_finish2: espFinish2Input })
                  setEspFinish2Input("")
                }
              }}
            />
          </CardContent>
        </Card>

        {/* Penalty */}
        <SelectionCard<Penalty>
          title="Penalty"
          items={penalties}
          selectedItem={selectedPenalty}
          onSelect={setSelectedPenalty}
          getDisplayName={(p) => `${p.type ?? 'Penalty'} (${p.amount}s)`}
        />

        <ConnectionStatusCard
          status={connectionStatus}
          setStatus={setConnectionStatus}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 mb-4 gap-6">
        <NumberInputCard
          title="Penalty Count"
          value={penaltyCount}
          onChange={(value) => SetPenaltyCount(value ?? 0)}
          placeholder="Amount of Penalties"
          kind="int"
        />

        <SelectionCard<Driver>
          title="Drivers"
          items={drivers}
          selectedItem={selectedDriver}
          onSelect={setSelectedDriver}
        />

        <NumberInputCard
          title="Energy Consumption"
          value={energyConsumption}
          onChange={(value) => setEnergyConsumption(value ?? 0)}
          placeholder="Energy Consumption"
          kind="float"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 mb-4 gap-6">
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Timestamps</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <TimestampSelector
              label="Start timestamp"
              timestamps={startTimestamps}
              selectedTimestamps={selectedStartTimestamps ?? []}
              setSelectedTimestamps={setSelectedStartTimestamps}
            />

            <TimestampSelector
              label="End timestamp"
              timestamps={endTimestamps}
              selectedTimestamps={selectedEndTimestamps ?? []}
              setSelectedTimestamps={setSelectedEndTimestamps}
            />
          </CardContent>
        </Card>

        <FormulaCard
          medianStartTimestamp={medianStartTimestamp}
          medianEndTimestamp={medianEndTimestamp}
          manualAttemptTime={manualAttemptTime}
          penaltyCount={penaltyCount}
          selectedPenaltyAmount={selectedPenalty?.amount ?? 0}
          setManualTimestamp={setManualAttemptTime}
        />

        <AttemptResultCard
          selectedTeam={selectedTeam}
          selectedDriver={selectedDriver}
          selectedChallenge={selectedChallenge}
          medianStartTimestamp={medianStartTimestamp}
          medianEndTimestamp={medianEndTimestamp}
          manualAttemptTime={manualAttemptTime}
          energyConsumption={energyConsumption}
          selectedPenalty={selectedPenalty}
          penaltyCount={penaltyCount}
          onSubmitSuccess={resetForm}
        />
      </div>
    </div>
  );
}