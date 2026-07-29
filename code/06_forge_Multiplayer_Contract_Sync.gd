```csharp
using System;
using System.Collections.Generic;
using Unity.Netcode;
using UnityEngine;

public class MultiplayerContractSyncSystem : NetworkBehaviour
{
    public struct ContractData : INetworkSerializable, IEquatable<ContractData>
    {
        public ulong Timestamp;
        public string[] Contracts;

        public void NetworkSerialize<T>(BufferSerializer<T> serializer) where T : IReaderWriter
        {
            serializer.SerializeValue(ref Timestamp);
            serializer.SerializeValue(ref Contracts);
        }

        public bool Equals(ContractData other)
        {
            return Timestamp == other.Timestamp && Contracts.SequenceEqual(other.Contracts);
        }
    }

    private static readonly TimeSpan DailyResetTime = new TimeSpan(0, 0, 30); // 30 seconds for testing
    private static DateTime _nextContractGeneration = DateTime.UtcNow.Add(DailyResetTime);

    [SerializeField] private NetworkVariable<ContractData> _contractData = new NetworkVariable<ContractData>();

    public override void OnNetworkSpawn()
    {
        base.OnNetworkSpawn();

        if (IsServer)
        {
            StartCoroutine(GenerateContracts());
        }

        // Sync current contracts with clients
        _contractData.Value = LoadContracts();
    }

    private void GenerateContracts()
    {
        while (true)
        {
            DateTime now = DateTime.UtcNow;

            TimeSpan timeToWait = _nextContractGeneration - now;
            if (timeToWait > TimeSpan.Zero)
            {
                System.Threading.Tasks.Task.Delay(timeToWait).GetAwaiter().GetResult();
            }

            GenerateDailyContracts();

            // Update all clients with new contract data
            _contractData.Value = LoadContracts();

            _nextContractGeneration = DateTime.UtcNow.Add(DailyResetTime);
        }
    }

    private void GenerateDailyContracts()
    {
        ContractData contractData = new ContractData
        {
            Timestamp = (ulong)(DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalSeconds,
            Contracts = new string[10] // Replace with actual contract generation logic
        };

        for (int i = 0; i < 10; i++)
        {
            contractData.Contracts[i] = $"Contract_{i}_{Guid.NewGuid()}";
        }

        SaveContracts(contractData);
    }

    private ContractData LoadContracts()
    {
        // Implement logic to load contracts from persistent storage
        return new ContractData { Timestamp = 0, Contracts = new string[10] };
    }

    private void SaveContracts(ContractData contractData)
    {
        // Implement logic to save contracts to persistent storage
    }

    public override void OnNetworkDespawn()
    {
        base.OnNetworkDespawn();

        // Save current contract data before shutdown
        SaveContracts(_contractData.Value);
    }
}
```