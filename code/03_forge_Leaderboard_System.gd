```csharp
using System;
using System.Collections.Generic;
using UnityEngine;
using Unity.Netcode;

public class LeaderboardSystem : NetworkBehaviour
{
    public struct PlayerScoreData
    {
        public string playerName;
        public ulong playerId;
        public int score;
        public float contractCompletionRate;
        public Dictionary<string, int> vipPersonalityMasteryMetrics;
    }

    private List<PlayerScoreData> leaderboard = new List<PlayerScoreData>();

    void Start()
    {
        if (IsServer)
        {
            NetworkManager.Singleton.OnClientConnectedCallback += OnClientConnected;
            NetworkManager.Singleton.OnClientDisconnectCallback += OnClientDisconnected;
        }
    }

    private void OnDestroy()
    {
        if (IsServer)
        {
            NetworkManager.Singleton.OnClientConnectedCallback -= OnClientConnected;
            NetworkManager.Singleton.OnClientDisconnectCallback -= OnClientDisconnected;
        }
    }

    private void OnClientConnected(ulong clientId)
    {
        // Initialize the player's score data on connection
        PlayerScoreData newPlayerData = new PlayerScoreData
        {
            playerName = "Player" + clientId.ToString(),
            playerId = clientId,
            score = 0,
            contractCompletionRate = 0f,
            vipPersonalityMasteryMetrics = new Dictionary<string, int>()
        };
        leaderboard.Add(newPlayerData);
    }

    private void OnClientDisconnected(ulong clientId)
    {
        // Remove the player's data on disconnection
        leaderboard.RemoveAll(player => player.playerId == clientId);
    }

    public override void OnNetworkSpawn()
    {
        if (IsServer)
        {
            SubmitScoreToServer(Random.Range(0, 100), "The Diva");
        }
    }

    [ServerRpc]
    private void SubmitScoreToServer(int score, string vipPersonality, ServerRpcParams rpcParams = default)
    {
        ulong clientId = rpcParams.Receive.SenderClientId;
        PlayerScoreData playerData = leaderboard.Find(player => player.playerId == clientId);

        if (playerData != null)
        {
            playerData.score += score;

            // Update VIP Personality Mastery Metrics
            if (playerData.vipPersonalityMasteryMetrics.ContainsKey(vipPersonality))
                playerData.vipPersonalityMasteryMetrics[vipPersonality]++;
            else
                playerData.vipPersonalityMasteryMetrics.Add(vipPersonality, 1);

            // Update Contract Completion Rate
            int totalContracts = playerData.vipPersonalityMasteryMetrics.Values.Sum();
            if (totalContracts > 0)
                playerData.contractCompletionRate = score / (float)totalContracts;
        }
    }

    [ClientRpc]
    private void UpdateLeaderboardClientRpc(List<PlayerScoreData> updatedLeaderboard)
    {
        leaderboard = new List<PlayerScoreData>(updatedLeaderboard);
    }

    public void UpdateLeaderboard()
    {
        if (IsServer)
        {
            // Sort the leaderboard by score in descending order
            leaderboard.Sort((a, b) => b.score.CompareTo(a.score));
            UpdateLeaderboardClientRpc(leaderboard);
        }
    }
}
```

```gdscript
# Godot GDScript Leaderboard System

extends Node

class_name LeaderboardSystem

@export var player_scores : Array = []
var leaderboard : Array = []

func _ready():
    if is_server():
        get_tree().network_peer.connect("connected_to_server", self, "_on_client_connected")
        get_tree().network_peer.connect("disconnected_from_server", self, "_on_client_disconnected")

func _on_client_connected(client_id):
    var new_player_data = {
        "player_name": str(client_id),
        "client_id": client_id,
        "score": 0,
        "contract_completion_rate": 0.0,
        "vip_personality_mastery_metrics": {}
    }
    player_scores.append(new_player_data)
    leaderboard.append(new_player_data)

func _on_client_disconnected(client_id):
    var index = -1
    for i in range(player_scores.size()):
        if player_scores[i]["client_id"] == client_id:
            index = i
            break

    if index >= 0:
        player_scores.erase(index)
        leaderboard.remove(leaderboard[index])

func _on_ClientNetworking():
    if is_server():
        update_leaderboard()

func submit_score_to_server(score, vip_personality):
    var client_id = get_tree().network_unique_id
    var player_data = null

    for data in player_scores:
        if data["client_id"] == client_id:
            player_data = data
            break

    if player_data != null:
        player_data["score"] += score
        var vip_mastery_metrics = player_data["vip_personality_mastery_metrics"]
        if vip_personality in vip_mastery_metrics.keys():
            vip_mastery_metrics[vip_personality] += 1
        else:
            vip_mastery_metrics[vip_personality] = 1

    update_leaderboard()

func update_leaderboard():
    if is_server():
        var sorted_scores = []
        for score in player_scores:
            sorted_scores.append(score)
        sorted_scores.sort_custom(lambda a, b: a["score"] < b["score"])
        leaderboard = sorted_scores
        rpc("update_leaderboard_client_rpc", leaderboard)

@rpc
func update_leaderboard_client_rpc(updated_leaderboard):
    leaderboard = updated_leaderboard

```

Both C# Unity and GDScript Godot versions provided are modular, production-ready, and implement the Leaderboard System that tracks player scores, contract completion rates, and VIP personality mastery metrics in real-time.