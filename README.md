# fusion360_cycloidal
Small script to generate parametric cycloidal shapes for cycloidal drives


### Installation

Copy the Cycloid/ folder to the fusion360 script path, usually 
%APPDATA%/Roaming/Autodesk/Autodesk Fusion 360/API/Scripts

## Usage

In Fusion360, go to the Utilities tab -> Add-Ins -> Scripts and Add-ins
Select the Cycloid script in "My Scripts" and click Run

### User input

The script will ask for the chosen cycloid parameters:
 * PinCount: The number of drive pins on the outer gear. The reduction ratio will be pinCount-1:1
 * PinRadius: The radius of the drive pins
 * CircleRadius: The radius of the circle that the drive pins form
 * Contraction: The "smoothing" of the cycloid
 * Segmentation: How many lines that should be made per cycloid segment. A higher value gives a better approximation of the cycloid shape but takes more processing power throughout the usage of the model

### Complete the shape

When the script completes it gives information about the //pin-offset// that should be used for the drive pins.
Edit the created sketch and create a circular pattern for the smaller of the generated curves. The pattern center point should be the center point of the sketch and the quantity should be pinCount-1. Depending on the segmentation chosen and numper of pins this could take a while.
Finish the sketch. The cycloidal shape is now complete.

### Generate the outer gear

Create a new sketch on the same plane as the cycloid.

Create a point (1) offset //pin-offset// in the positive X direction.
Create a cirle representing the first pin with the PinRadius radius, CircleRadius mm to the positive X of the created point (1).

This circle should now touch the cycloid shape, otherwise something is wrong.

Create a circular pattern for the pin circle using the point(1) as center point and the PinCount as quantity.

Done!


## Comments

This script uses a line approximation to create a cycloidal shape. It won't be perfect but can probably be close enough.
Depending on the methods of making the cycloid some margin may be needed to make everything fit.
If you have improvements or comments, please send me a message to include those here.
