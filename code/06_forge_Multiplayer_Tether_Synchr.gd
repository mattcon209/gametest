```csharp
using UnityEngine;
using Unity.Netcode;

public class Tether : NetworkBehaviour
{
    public Transform bodyguardTransform;
    public Transform vipTransform;
    public float maxLength = 5f;
    public float springDamping = 0.1f;
    public float springStrength = 20f;

    private LineRenderer lineRenderer;
    private SpringJoint springJoint;
    private bool isClient;

    void Start()
    {
        if (!IsServer)
        {
            isClient = true;
            return;
        }

        lineRenderer = gameObject.AddComponent<LineRenderer>();
        lineRenderer.positionCount = 2;
        lineRenderer.useWorldSpace = false;
        springJoint = gameObject.AddComponent<SpringJoint>();

        UpdateTether();
    }

    void Update()
    {
        if (isClient) return;

        UpdateTether();
    }

    private void UpdateTether()
    {
        var bodyguardPosition = bodyguardTransform.position;
        var vipPosition = vipTransform.position;

        float distance = Vector3.Distance(bodyguardPosition, vipPosition);
        springJoint.connectedBody = vipTransform.GetComponent<Rigidbody>();
        springJoint.spring = springStrength;
        springJoint.damper = springDamping;

        lineRenderer.SetPosition(0, bodyguardPosition);
        lineRenderer.SetPosition(1, vipPosition);

        if (distance > maxLength)
        {
            float tension = distance - maxLength;
            ServerRpcParams rpcParams = new ServerRpcParams();
            TetherTensionServerRpc(tension, rpcParams);
        }
    }

    [ServerRpc]
    private void TetherTensionServerRpc(float tension, ServerRpcParams rpcParams)
    {
        ClientsForEach((clientId) =>
        {
            if (rpcParams.Receive.SenderClientId == clientId)
                return;

            TetherTensionClientRpc(tension);
        });
    }

    [ClientRpc]
    private void TetherTensionClientRpc(float tension)
    {
        // Apply tension logic on clients
        Debug.Log("Received tether tension: " + tension);

        // Handle other tether states and tangle resolution here...
    }
}
```