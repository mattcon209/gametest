```csharp
using UnityEngine;
using System.Collections;

public class VIPPanicPathfindingOverride : MonoBehaviour
{
    public VIPController vipController;
    public float panicThreshold = 80f; // Stress meter threshold to trigger panic
    public float panicDuration = 5f; // Duration of the panic state
    private bool isPanicActive = false;

    void Update()
    {
        if (vipController.stressMeter >= panicThreshold && !isPanicActive)
        {
            StartCoroutine(PanicPathfindingOverride());
        }
    }

    IEnumerator PanicPathfindingOverride()
    {
        isPanicActive = true;
        Vector3 originalDestination = vipController.destination;

        // Generate a new random destination within the panic range
        float panicRange = 10f; // Adjustable panic range radius
        Vector3 panicDestination = originalDestination + new Vector3(
            Random.Range(-panicRange, panicRange),
            0,
            Random.Range(-panicRange, panicRange)
        );

        vipController.destination = panicDestination;

        yield return new WaitForSeconds(panicDuration);

        // Reset to the original destination
        vipController.destination = originalDestination;
        isPanicActive = false;
    }
}
```

```gdscript
extends Node

@export var vip_controller: VIPController
@export var panic_threshold: float = 80.0 # Stress meter threshold to trigger panic
@export var panic_duration: float = 5.0 # Duration of the panic state

var is_panic_active: bool = false

func _process(delta):
    if vip_controller.stress_meter >= panic_threshold and not is_panic_active:
        yield(self, "PanicPathfindingOverride")

func PanicPathfindingOverride():
    is_panic_active = true
    var original_destination = vip_controller.destination

    # Generate a new random destination within the panic range
    var panic_range: float = 10.0 # Adjustable panic range radius
    var panic_destination = original_destination + Vector3(
        randf_range(-panic_range, panic_range),
        0,
        randf_range(-panic_range, panic_range)
    )

    vip_controller.destination = panic_destination

    yield(get_tree(), "process_frame")
    yield(get_tree().create_timer(panic_duration), "timeout")

    # Reset to the original destination
    vip_controller.destination = original_destination
    is_panic_active = false
```