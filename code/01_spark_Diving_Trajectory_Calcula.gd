```csharp
using UnityEngine;

public class DivingTrajectoryCalculator : MonoBehaviour
{
    public float diveSpeed = 10f;
    public LayerMask obstacleLayer;

    private Rigidbody rb;
    private RaycastHit hitInfo;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Dive();
        }
    }

    void Dive()
    {
        // Reset velocity to start a new dive
        rb.velocity = Vector3.zero;
        rb.AddForce(Vector3.down * diveSpeed, ForceMode.Impulse);
        
        PredictDivePath();
    }

    void PredictDivePath()
    {
        for (float t = 0.1f; t < 5f; t += Time.deltaTime)
        {
            Vector3 position = transform.position + rb.velocity * t;
            if (Physics.Raycast(position, Vector3.down, out hitInfo, diveSpeed * Time.deltaTime, obstacleLayer))
            {
                Debug.DrawLine(position, hitInfo.point, Color.red);
                break;
            }
        }
    }

    void OnCollisionEnter(Collision collision)
    {
        if ((obstacleLayer & (1 << collision.gameObject.layer)) != 0)
        {
            // Handle collision with obstacles
            rb.velocity = Vector3.zero;
            Debug.Log("Collision detected with obstacle!");
        }
    }
}
```