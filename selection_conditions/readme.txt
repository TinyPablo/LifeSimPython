Adding a New Selection Condition
--------------------------------

1. Create the condition file:
   - Go to the /selection_conditions/ folder.
   - Copy an existing condition file (e.g., bottom_right_square.py) and rename it to your desired condition name.
   - Open your new file and implement a function:

     def condition(x, y, w, h) -> bool:
         # Return True if the (x, y) point meets your selection condition
         # x, y = coordinates of the point
         # w, h = width and height of the area
         ...

2. Add it to the enum:
   - Open /selection_conditions/enum.py.
   - Add a new entry for your condition inside SelectionCondition, like this:

     class SelectionCondition(Enum):
         ...
         YOUR_CONDITION_NAME = "your_condition_name"

3. Done! Your new selection condition is now available for use.
