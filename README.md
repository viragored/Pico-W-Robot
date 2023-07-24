# Pico-W-Robot
## Micropython code to control a basic robot using a web interface
### File 4WD.py: For a Pico W
First attempt, using L298N motor driver on a Dagu multi-chassis (4WD version)

Uses 2 pairs of DC motors from the Dagu kit in parallel, PWM speed control, power from 3S LiPo battery and driver board's voltage converter. Low torque at low speed, not very satisfactory.

Web interface accessed from browser provides control - there can be big time lags between pressing a button and the robot responding

### File "4WD_BT_DRV8833": For a basic Pico (not W) with HC-05 Bluetooth module
Same chassis but with a DRV8833 motor driver and a Buck step-dowm voltage converter delivering 5V (measured at 5.02V). Platform on top of Dagu metal chassis designed in OpenSCAD, printed in PLA on a Prusa i3 Mk3S

Pictures "front" and "back" show the first prototype print.

Control is via Bluetooth, with an Android app designed with MIT App Inventor - https://ai2.appinventor.mit.edu/ 

It took me a while to work out that to control the motors via DRV8833 using pulse width modulation, and to avoid the back-EMF from the motors burning out the electronics, I needed to use a mix of PWM and PIN.Out instructions. It's clunky, but the maximum voltage I've measured during testing with this code is 5.11V. Using all PWM instructions I had measured 6.6V - which blew a neopixel I was using. Had the Pico been powered from that circuit and not the USB it too would have blown.

With Bluetooth control, response is virtually instant.

### Android App File "Robotdriver.apk": 
There is a screenshot of the app in file "App screenshot.jpg"
Simple usage instructions are:
- Install the app on your mobile device
- Pair your mobile device and the HC-05 (default password is probably 1234)
- Run the app. Tap the prompt to 'Select device' and choose the HC-05. Wait for the LED on the HC-05 to turn off when pairing is complete
- Playtime! Move the robot forward, backwards, left or right with the arrows. Adjust the speed with the slider. Stop the robot with "Stop", and resume movement with the arrows.
- The "Crash stop" button stops the motors, and terminates the code on the Pico. If using main.py, it might be possible at this point to connect Thonny and access the Pico to edit the code (not yet tested). 

**Inspiration from:**

- https://www.youtube.com/watch?v=H1Fzil_VUq4 
- https://www.youtube.com/watch?v=iTo4Qh2R6m4 
- https://www.youtube.com/@NerdCaveYT
- https://www.youtube.com/watch?v=U4unGGNjFBg 
