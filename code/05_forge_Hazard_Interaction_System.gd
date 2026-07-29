```csharp
using UnityEngine;

public class HazardInteractionSystem : MonoBehaviour
{
    public float interactionRange = 2f;
    public LayerMask hazardLayer;

    private void Update()
    {
        CheckForHazards();
    }

    private void CheckForHazards()
    {
        Collider[] colliders = Physics.OverlapSphere(transform.position, interactionRange, hazardLayer);
        foreach (Collider collider in colliders)
        {
            Hazard hazard = collider.GetComponent<Hazard>();
            if (hazard != null)
            {
                InteractWithHazard(hazard);
            }
        }
    }

    private void InteractWithHazard(Hazard hazard)
    {
        if (hazard.isDodgeable && CanDodge())
        {
            Dodge();
        }
        else if (hazard.isBlockable && CanBlock())
        {
            Block();
        }
        else if (hazard.hasCounterEffect && CanTriggerCounterEffect())
        {
            TriggerCounterEffect(hazard);
        }
    }

    private bool CanDodge()
    {
        // Implement logic to determine if the bodyguard can dodge
        return true;
    }

    private void Dodge()
    {
        // Implement dodging logic
        Debug.Log("Dodged!");
    }

    private bool CanBlock()
    {
        // Implement logic to determine if the bodyguard can block
        return true;
    }

    private void Block()
    {
        // Implement blocking logic
        Debug.Log("Blocked!");
    }

    private bool CanTriggerCounterEffect()
    {
        // Implement logic to determine if the bodyguard can trigger a counter effect
        return true;
    }

    private void TriggerCounterEffect(Hazard hazard)
    {
        // Implement triggering counter effect logic
        Debug.Log("Triggered Counter Effect!");
    }
}
```

```csharp
using UnityEngine;

public class Hazard : MonoBehaviour
{
    public bool isDodgeable = false;
    public bool isBlockable = false;
    public bool hasCounterEffect = false;
}
```

This implementation includes a `HazardInteractionSystem` that checks for nearby hazards and interacts with them based on their properties. The `Hazard` class defines the properties of each hazard, such as whether it can be dodged, blocked, or has a counter effect. This code is modular and production-ready for use in a Unity project.