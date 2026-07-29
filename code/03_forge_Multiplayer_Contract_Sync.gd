```csharp
using System.Collections.Generic;
using UnityEngine;

public class MultiplayerContractSync : MonoBehaviour
{
    public static MultiplayerContractSync Instance { get; private set; }

    [SerializeField] private List<string> dailyContracts = new List<string>();
    [SerializeField] private int currentContractIndex = 0;

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(this);
        }
        else
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
    }

    public void SyncContractsWithServer(List<string> serverContracts, int serverContractIndex)
    {
        dailyContracts = new List<string>(serverContracts);
        currentContractIndex = serverContractIndex;

        // Trigger UI update or other necessary actions
        OnContractsSynced();
    }

    public void PushLocalChangesToServer()
    {
        if (NetworkManager.IsConnected())
        {
            NetworkManager.Instance.SendDataToServer(dailyContracts, currentContractIndex);
        }
    }

    private void OnContractsSynced()
    {
        // Trigger any UI updates or other necessary actions
        Debug.Log("Contracts Synced: " + string.Join(", ", dailyContracts));
        Debug.Log("Current Contract Index: " + currentContractIndex);
    }
}
```