```csharp
using UnityEngine;

public class DivingTrajectory : MonoBehaviour
{
    public float diveSpeed = 10f;
    public float gravity = 9.81f;
    private Vector3 initialPosition;
    private Vector3 targetPosition;
    private bool isDiving = false;
    private float horizontalVelocity;
    private float verticalVelocity;

    void Update()
    {
        if (isDiving)
        {
            CalculateParabolicTrajectory();
        }
    }

    public void StartDive(Vector3 startPosition, Vector3 endPosition)
    {
        initialPosition = startPosition;
        targetPosition = endPosition;
        isDiving = true;

        // Calculate initial velocity components
        float distance = Vector3.Distance(startPosition, endPosition);
        float timeToTarget = distance / diveSpeed;
        horizontalVelocity = distance / timeToTarget;
        verticalVelocity = Mathf.Sqrt(2 * gravity * (initialPosition.y - targetPosition.y));
    }

    void CalculateParabolicTrajectory()
    {
        // Update position based on parabolic trajectory
        Vector3 direction = (targetPosition - initialPosition).normalized;
        horizontalVelocity *= direction.x;
        verticalVelocity -= gravity * Time.deltaTime;

        transform.position += new Vector3(horizontalVelocity, verticalVelocity, 0) * Time.deltaTime;

        // Check if we've reached the target
        if (Vector3.Distance(transform.position, targetPosition) < 1f)
        {
            isDiving = false;
        }
    }

    void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawLine(initialPosition, targetPosition);
    }
}
```