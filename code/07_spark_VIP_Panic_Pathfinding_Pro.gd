```csharp
using System.Collections.Generic;
using UnityEngine;

public class VipPanicPathfinder : MonoBehaviour
{
    public float panicThreshold = 50f; // Stress threshold to trigger panic mode
    public float escapeSpeed = 5f; // Speed when escaping
    private List<GameObject> obstacles = new List<GameObject>();
    private bool isPanicMode = false;
    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        InvokeRepeating("CheckStress", 1f, 1f); // Check stress every second
    }

    void Update()
    {
        if (isPanicMode)
        {
            Escape();
        }
    }

    void CheckStress()
    {
        float currentStress = GetComponent<VipStressMeter>().GetCurrentStress(); // Assuming a VipStressMeter component exists

        if (currentStress >= panicThreshold && !isPanicMode)
        {
            EnterPanicMode();
        }
        else if (currentStress < panicThreshold && isPanicMode)
        {
            ExitPanicMode();
        }
    }

    void EnterPanicMode()
    {
        isPanicMode = true;
        FindObstacles(); // Detect nearby obstacles
    }

    void ExitPanicMode()
    {
        isPanicMode = false;
    }

    void Escape()
    {
        Vector3 direction = FindSafeDirection();
        if (direction != Vector3.zero)
        {
            rb.velocity = direction * escapeSpeed;
        }
    }

    Vector3 FindSafeDirection()
    {
        foreach (GameObject obstacle in obstacles)
        {
            Vector3 avoidanceDir = (transform.position - obstacle.transform.position).normalized;
            RaycastHit hit;

            // Check if the direction is clear of other obstacles
            if (!Physics.Raycast(transform.position, avoidanceDir, out hit, 10f))
            {
                return avoidanceDir;
            }
        }

        return Vector3.zero; // No safe direction found
    }

    void FindObstacles()
    {
        Collider[] colliders = Physics.OverlapSphere(transform.position, 10f);
        obstacles.Clear();
        foreach (Collider col in colliders)
        {
            if (col.gameObject.CompareTag("Obstacle") && col != GetComponent<Collider>())
            {
                obstacles.Add(col.gameObject);
            }
        }
    }
}
```