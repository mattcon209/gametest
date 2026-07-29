```csharp
using UnityEngine;

public class DivingSlowMotionCameraSystem : MonoBehaviour
{
    public Animator animator;
    public float slowMotionFactor = 0.1f; // Adjust this value for desired slow-motion effect
    private bool isDiving = false;
    private float originalTimeScale;
    private float originalFixedDeltaTime;

    void Start()
    {
        if (animator == null)
            animator = GetComponent<Animator>();

        originalTimeScale = Time.timeScale;
        originalFixedDeltaTime = Time.fixedDeltaTime;
    }

    void Update()
    {
        if (!isDiving) return;

        // Check for diving animation
        AnimatorStateInfo stateInfo = animator.GetCurrentAnimatorStateInfo(0);
        if (stateInfo.IsName("Dive"))
        {
            ApplySlowMotion();
        }
        else
        {
            ResetTimeScale();
        }
    }

    void ApplySlowMotion()
    {
        Time.timeScale = slowMotionFactor;
        Time.fixedDeltaTime = originalFixedDeltaTime * slowMotionFactor;
    }

    void ResetTimeScale()
    {
        Time.timeScale = originalTimeScale;
        Time.fixedDeltaTime = originalFixedDeltaTime;
    }
}
```