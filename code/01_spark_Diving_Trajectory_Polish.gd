```csharp
using System.Collections;
using UnityEngine;

public class DiveTrajectory : MonoBehaviour
{
    public float diveSpeed = 5f;
    public float diveDuration = 2f;
    public LayerMask groundLayer;

    private Rigidbody rb;
    private Vector3 diveStartPos;
    private Quaternion diveStartRot;
    private Coroutine diveCoroutine;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            StartDive();
        }
    }

    public void StartDive()
    {
        if (diveCoroutine != null)
        {
            StopCoroutine(diveCoroutine);
        }

        diveStartPos = transform.position;
        diveStartRot = transform.rotation;

        diveCoroutine = StartCoroutine(DiveRoutine());
    }

    IEnumerator DiveRoutine()
    {
        float elapsedTime = 0f;
        Vector3 targetPosition = diveStartPos + (transform.forward * diveSpeed * diveDuration);

        while (elapsedTime < diveDuration)
        {
            elapsedTime += Time.deltaTime;

            Vector3 newPosition = Vector3.Lerp(diveStartPos, targetPosition, elapsedTime / diveDuration);
            Quaternion newRotation = Quaternion.Slerp(diveStartRot, transform.rotation, elapsedTime / diveDuration);

            rb.MovePosition(newPosition);
            rb.MoveRotation(newRotation);

            if (Physics.Raycast(transform.position + (transform.up * 0.5f), -transform.up, out RaycastHit hitInfo, 1f, groundLayer))
            {
                rb.velocity = Vector3.zero;
                transform.position = hitInfo.point + (Vector3.up * 0.1f);
                break;
            }

            yield return null;
        }

        diveCoroutine = null;
    }
}
```