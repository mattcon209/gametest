```csharp
using UnityEngine;

public class VipPanicBehavior : MonoBehaviour
{
    public float panicThreshold = 0.8f; // Stress level threshold to enter panic mode
    public float panicSpeedMultiplier = 1.5f; // Speed multiplier when in panic mode
    public float obstacleAvoidanceRadius = 2f; // Radius for detecting obstacles
    public LayerMask obstacleLayer; // Layer mask for detecting obstacles

    private AIPathfinding pathfinding;
    private CharacterController controller;
    private float currentStress = 0f;

    void Start()
    {
        pathfinding = GetComponent<AIPathfinding>();
        controller = GetComponent<CharacterController>();

        // Subscribe to stress level updates
        StressManager.Instance.onStressLevelChanged += UpdateStressLevel;
    }

    void UpdateStressLevel(float newStress)
    {
        currentStress = newStress;

        if (currentStress >= panicThreshold && !pathfinding.IsInPanicMode())
        {
            EnterPanicMode();
        }
        else if (currentStress < panicThreshold && pathfinding.IsInPanicMode())
        {
            ExitPanicMode();
        }
    }

    void EnterPanicMode()
    {
        pathfinding.SetSpeedMultiplier(panicSpeedMultiplier);
        pathfinding.EnablePanicMode(true);

        // Start obstacle avoidance
        StartCoroutine(AvoidObstacles());
    }

    void ExitPanicMode()
    {
        pathfinding.SetSpeedMultiplier(1f);
        pathfinding.EnablePanicMode(false);
    }

    IEnumerator AvoidObstacles()
    {
        while (pathfinding.IsInPanicMode())
        {
            Collider[] obstacles = Physics.OverlapSphere(transform.position, obstacleAvoidanceRadius, obstacleLayer);

            foreach (var obstacle in obstacles)
            {
                Vector3 avoidanceDirection = (transform.position - obstacle.transform.position).normalized;
                pathfinding.AvoidObstacle(obstacle.transform.position, avoidanceDirection);
            }

            yield return new WaitForSeconds(0.2f); // Adjust the interval as needed
        }
    }
}
```