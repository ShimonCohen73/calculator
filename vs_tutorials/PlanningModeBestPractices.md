# Planning Mode Best Practices

This guide provides key learnings and best practices for effectively using Claude Code's planning mode to achieve better outcomes.

## Overview

Planning mode is a powerful feature that allows Claude to design an implementation approach before writing code. However, the quality of the plan depends heavily on the clarity and detail of your requirements.

## Key Lesson Learned

**"When working in planning mode, I should be much more detailed in my request and work in smaller tasks."**

The more specific and detailed your requirements, the better the plan will match your actual expectations.

## Best Practices

### 1. Start with a Clear Vision

Before entering plan mode, write down exactly what you want:

#### Define the UI/UX
- **Exact visual layout** - Where should elements appear?
- **User interactions** - Buttons? Keyboard shortcuts? Mouse gestures?
- **Visual appearance** - Colors, sizes, positioning
- **Workflow examples** - Step-by-step user actions from start to finish

#### Example - Poor Request:
```
"Add programmer mode to the calculator"
```

#### Example - Good Request:
```
"Add programmer mode with:
- A toggle button in the bottom-right labeled 'BIN/DEC'
- When clicked, show hex digit buttons (A-F) below the number pad
- Display results in both decimal and hex below the main display
- Add keyboard shortcuts: Ctrl+H for hex mode
- Bitwise AND button (labeled '&') replaces the '=' button in this mode
```

### 2. Break Into Small, Testable Tasks

Instead of requesting one large feature, break it down into incremental steps:

#### Large Task (Avoid):
- "Implement complete programmer mode with all features"

#### Small Tasks (Better):
```
Task 1: Add a single bitwise AND operation
  - Add bitwise_and() function to core.py
  - Write tests for the function
  - Verify it works with simple integers

Task 2: Add an AND button to the GUI
  - Add button to layout
  - Wire it to the function
  - Test the button works

Task 3: Add hex input parsing
  - Parse 0xFF format
  - Add tests
  - Display hex results

Task 4: Add multi-base display panel
  - Create display widget
  - Format output in DEC/HEX/OCT/BIN
  - Position it correctly
```

### 3. Provide Context and Examples

Help Claude understand your vision by providing:

#### Reference Materials
- Screenshots of similar interfaces
- Links to calculators with the features you want
- Mockups or sketches (even hand-drawn)
- Examples from other applications

#### Concrete Examples
```
"When I type '12 & 10' and press Enter:
- Main display shows: 8
- Below it shows:
  DEC: 8
  HEX: 0x8
  OCT: 0o10
  BIN: 0b1000"
```

### 4. Use AskUserQuestion in Plan Mode

When Claude enters plan mode, it should ask clarifying questions like:

- "Do you want buttons for bitwise operators or keyboard input?"
- "Should the display be read-only or editable?"
- "Do you want a Windows Calculator-style interface or custom design?"
- "Should there be hex digit buttons (A-F) for direct input?"
- "Where should the multi-base display appear?"

**Encourage this!** If the plan doesn't ask questions, it's making assumptions.

### 5. Review the Plan Before Executing

When you see the plan via `ExitPlanMode`, you can:

#### Option 1: Approve
- "Yes, proceed with this plan"

#### Option 2: Reject with Feedback
- "No, I want buttons instead of typing"
- "No, the layout should be different"
- "No, let's focus on just the AND operation first"

#### Option 3: Request Modifications
- "Good start, but add hex input buttons (A-F)"
- "Update the plan to include keyboard shortcuts"
- "Change the display from read-only to editable"

### 6. Iterate on Requirements

Don't expect perfection on the first try:

```
Round 1: "Add programmer mode"
Result: Not what you wanted

Round 2: "Add programmer mode with Windows Calculator layout:
- Bottom section switches between standard and programmer modes
- Programmer mode shows: HEX/DEC/OCT/BIN radio buttons
- Add bitwise buttons: AND, OR, XOR, NOT, LSH, RSH
- Display shows result in all bases simultaneously"
Result: Much better!
```

## Common Pitfalls to Avoid

### ❌ Vague Requirements
```
"Make it work like a real programmer calculator"
```
**Problem:** "Real" is ambiguous - Windows? macOS? Scientific calculator?

### ❌ Assuming Claude Knows Your Vision
```
"Add the obvious bitwise features"
```
**Problem:** What's "obvious" varies by person and context

### ❌ Not Specifying UI Details
```
"Add buttons for operations"
```
**Problem:** Where? What size? What color? Which operations?

### ❌ Too Large in Scope
```
"Implement full programming calculator with all features from Windows, macOS, and HP scientific calculators"
```
**Problem:** Overwhelming scope, unclear priorities

## Checklist Before Entering Plan Mode

- [ ] I can describe the exact UI layout I want
- [ ] I have examples of the user workflow
- [ ] I know which interactions should be buttons vs keyboard
- [ ] I can specify where new UI elements should appear
- [ ] I've broken the feature into logical sub-tasks
- [ ] I have reference materials if needed
- [ ] I'm ready to answer clarifying questions
- [ ] I understand I can reject the plan and iterate

## Example: Good Planning Request

```markdown
# Feature Request: Programmer Mode

## Overview
Add a programmer mode toggle to the calculator GUI that enables 
bitwise operations and multi-base number display.

## UI Layout
1. Add toggle button labeled "STD/PROG" at bottom-right (below "rad" button)
2. When PROG mode active:
   - Button highlight changes to bright purple
   - A new panel appears below the main display
   - Panel shows 4 labels in a row: "DEC: | HEX: | OCT: | BIN:"

## Buttons to Add
- Replace "√" with "&" (AND) in PROG mode
- Replace "%" with "|" (OR) in PROG mode  
- Replace "^" with "^" (XOR) - same symbol, different operation
- Add "<<" button where "." was
- Add ">>" button (new)
- Add "~" button for NOT (new)

## User Interaction Flow
1. User clicks STD/PROG button → mode toggles
2. In PROG mode, user clicks numbers: "1", "2"
3. User clicks "&" button
4. User clicks "1", "0"
5. User clicks "=" button
6. Display shows: "8"
7. Multi-base panel shows: "DEC: 8 | HEX: 0x8 | OCT: 0o10 | BIN: 0b1000"

## Input Format Support
- Decimal: 12, 255, etc.
- Hex: 0xFF, 0x0F, etc. (allow typing via keyboard)
- Octal: 0o77, 0o10, etc.
- Binary: 0b1010, 0b1111, etc.

## Technical Requirements
- Core operations in core.py: bitwise_and, bitwise_or, bitwise_xor, etc.
- All operations work only on integers
- Raise ValueError if non-integer in PROG mode
- Update CLI to support /prog command for mode toggle
- Add tests for all new operations

## Reference
Similar to Windows Calculator in Programmer mode, but simplified.
```

## Conclusion

**The key to successful planning is specificity.** The more detailed your requirements, the closer the implementation will match your vision. Don't hesitate to provide "too much" detail - it's better to be overly specific than leave things to interpretation.

Remember: **Claude can execute your vision, but it needs to understand that vision first.**

---

*Created from lessons learned during calculator programmer mode implementation*
*Date: 2026-05-27*
