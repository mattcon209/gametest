```csharp
using System.Collections;
using UnityEngine;

public class DivingAnimation : MonoBehaviour
{
    public Animator animator;
    public float diveSpeed = 5f;
    public float impactForce = 10f;
    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    public void Dive(Vector3 targetPosition)
    {
        StartCoroutine(DiveCoroutine(targetPosition));
    }

    IEnumerator DiveCoroutine(Vector3 targetPosition)
    {
        animator.SetTrigger("Dive");

        while (Vector3.Distance(transform.position, targetPosition) > 0.1f)
        {
            Vector3 direction = (targetPosition - transform.position).normalized;
            rb.velocity = direction * diveSpeed;

            yield return null;
        }

        // Impact effect
        rb.AddForce(Vector3.up * impactForce, ForceMode.Impulse);
        animator.SetTrigger("Impact");
    }
}
```