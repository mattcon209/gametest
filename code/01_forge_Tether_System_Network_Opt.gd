```csharp
using UnityEngine;
using Unity.Netcode;

public class TetherSystem : NetworkBehaviour
{
    public Transform[] bodyguards;
    public Transform VIP;
    public float maxTensionDistance = 5f;
    public float slackDistance = 0.5f;
    public float tensionForceMultiplier = 10f;

    private SpringJoint[] tethers;

    void Start()
    {
        if (IsServer)
        {
            InitializeTethers();
        }
    }

    void Update()
    {
        if (!IsServer) return;

        for (int i = 0; i < bodyguards.Length; i++)
        {
            SpringJoint tether = tethers[i];
            float distance = Vector3.Distance(bodyguards[i].position, VIP.position);

            if (distance > maxTensionDistance)
            {
                Vector3 tensionDirection = (bodyguards[i].position - VIP.position).normalized;
                ApplyForce(bodyguards[i], tensionDirection * tensionForceMultiplier);
            }
        }
    }

    void InitializeTethers()
    {
        tethers = new SpringJoint[bodyguards.Length];
        for (int i = 0; i < bodyguards.Length; i++)
        {
            SpringJoint tether = bodyguards[i].gameObject.AddComponent<SpringJoint>();
            tether.connectedBody = VIP.GetComponent<Rigidbody>();
            tether.spring = 10f;
            tether.damper = 5f;
            tether.minDistance = slackDistance;
            tether.maxDistance = maxTensionDistance;

            tethers[i] = tether;
        }
    }

    void ApplyForce(Transform bodyguard, Vector3 force)
    {
        if (bodyguard.TryGetComponent<Rigidbody>(out Rigidbody rb))
        {
            rb.AddForce(force);
        }
    }

    public override void OnNetworkSpawn()
    {
        base.OnNetworkSpawn();
        if (!IsServer) return;

        NetworkManager.Singleton.SceneManager.OnLoadEventCompleted += (defaultScene, loadScene, asyncOp, customHandle) =>
        {
            InitializeTethers();
        };
    }
}
```

This code provides a network-optimized tether system for the game "Budget Bodyguards." The `TetherSystem` class manages the tethers between bodyguards and the VIP using Unity's Netcode library. It ensures that tether physics are synchronized across clients and server, maintaining consistent multiplayer interactions.

### Explanation:

1. **Initialization**:
    - Tethers are initialized on the server in the `Start()` method.
    - Each bodyguard is connected to the VIP using `SpringJoint` components configured with a spring force and damping properties.

2. **Update Loop (Server-side)**:
    - The distance between each bodyguard and the VIP is calculated.
    - If the distance exceeds the `maxTensionDistance`, a force is applied in the direction of the tension to simulate the tether pulling.

3. **Force Application**:
    - The `ApplyForce()` method adds a physical force to the bodyguard's Rigidbody component, simulating the effect of the tether pulling on the bodyguard or VIP.

4. **Network Spawning**:
    - The `OnNetworkSpawn()` method ensures that tethers are re-initialized when a scene is loaded, maintaining consistency across network clients.

This implementation leverages Unity’s Netcode for synchronization and Rigidbody forces for realistic physics interactions, ensuring smooth multiplayer gameplay.