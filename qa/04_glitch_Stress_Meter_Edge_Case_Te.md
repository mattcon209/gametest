

**BUG REPORT: VIP Stress Meter Does Not Reset at Contract Start**

---

### **Bug ID:** VV-2023-05-GLITCH-14

### **Issue Category:** Stress Meter Mechanics

### **Severity Level:** Medium (Edge Case)

### **Description:**
The VIP stress meter fails to reset properly when transitioning to a new contract. After completing one contract, the stress meter retains residual values from the previous session, leading to incorrect stress accumulation and inconsistent gameplay.

### **Steps to Reproduce:**

1. Complete any daily contract.
2. Begin playing the next contract without restarting the game.
3. Observe the VIP's stress meter during the new contract; it carries over residual stress from the previous contract.
4. The issue is particularly noticeable when transitioning between contracts with varying stress triggers.

### **Expected Behavior:**
The stress meter should reset to 0% at the start of each new contract, ensuring that player performance metrics are independent of prior gameplay sessions.

### **Actual Behavior:**
Stress carries over from previous contracts, leading to misleading stress values and potential game balance issues.

### **Root Cause Analysis:**
1. **Missing Initialization:** The function responsible for resetting the stress meter (`ResetStress()`) is not called at the start of a new contract.
2. **State Persistence:** Variables tracking stress remain uninitialized or retain old values when transitioning to new contracts, causing carry-over.

---

### **Fix Implemented:**

Modify `GameManager.cs` to ensure `ResetStress()` is invoked at the beginning of each new contract:

```csharp
// In GameManager.cs, within the function that loads a new contract:
public void LoadNewContract()
{
    // Existing code...

    // FIX: Reset VIP stress meter when starting a new contract.
    if (VIPInstance != null)
    {
        VIPInstance.ResetStress();
    }

    // Remaining code...
}
```

---

### **Test Verification Steps:**

1. Play through multiple contracts without restarting the game.
2. Confirm that after each contract starts, the stress meter initializes at 0% and accumulates correctly based on new gameplay.

---

**Conclusion:** The fix ensures the VIP stress meter resets at the start of each contract, preventing residual values from affecting gameplay integrity.