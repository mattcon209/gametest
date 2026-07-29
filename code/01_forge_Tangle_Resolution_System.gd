```csharp
// TangleResolutionSystem.cs
using UnityEngine;

public class TangleResolutionSystem : MonoBehaviour
{
    public GameObject[] tethers; // Array of tether objects
    public float untangleThreshold = 0.1f; // Distance threshold for automatic untangling
    private bool isTangled = false;
    private GameObject tangledObject;

    void Update()
    {
        CheckForTangles();
        ManualUntangle();
    }

    void CheckForTangles()
    {
        foreach (var tether in tethers)
        {
            Collider[] hitColliders = Physics.OverlapSphere(tether.transform.position, untangleThreshold);
            foreach (var hitCollider in hitColliders)
            {
                if (hitCollider.gameObject != tether && !tether.GetComponent<Tether>().IsConnected(hitCollider.gameObject))
                {
                    isTangled = true;
                    tangledObject = hitCollider.gameObject;
                    break;
                }
            }

            if (!isTangled)
            {
                // Automatic untangling
                if (Vector3.Distance(tether.transform.position, tangledObject.transform.position) > untangleThreshold)
                {
                    Untangle();
                }
            }
        }
    }

    void ManualUntangle()
    {
        if (isTangled && Input.GetKeyDown(KeyCode.Space)) // Space key for manual untangling
        {
            Untangle();
        }
    }

    void Untangle()
    {
        if (tangledObject != null)
        {
            // Perform the untangling logic here
            Debug.Log("Untangling from " + tangledObject.name);
            isTangled = false;
            tangledObject = null;
        }
    }
}
```

```csharp
// Tether.cs
using UnityEngine;

public class Tether : MonoBehaviour
{
    public GameObject connectedTo; // The object this tether is connected to

    public bool IsConnected(GameObject obj)
    {
        return connectedTo == obj;
    }

    void Update()
    {
        if (connectedTo != null)
        {
            // Update the tether's position based on its connection
            transform.position = Vector3.Lerp(transform.position, connectedTo.transform.position, Time.deltaTime * 5f);
        }
    }
}
```

This code implements a basic Tangle Resolution System in C# for Unity. The `TangleResolutionSystem` script checks for tangles using collision detection and provides both automatic and manual untangling mechanisms. The `Tether` script manages the connection between tethers and their connected objects.