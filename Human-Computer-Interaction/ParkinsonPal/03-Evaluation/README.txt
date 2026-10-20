ParkinsonPal – HCI Project (Group08)
Figma Link:
https://www.figma.com/design/E0L2XanMxAwUJDKOXBzMUB/ParkinsonPal?node-id=0-1&p=f&t=jUPIMxbNXoE5ig7E-0


____________________________________________________________________________




Screenflow & Navigation:
* Home Screen Access (The home screen acts as the central hub). 


It links directly to:
* Track Your Symptoms
* Medication Manager
* Exercise & Therapy
* Brain Games


 Vertical Flows (Fully Implemented):
1. Register
2. Sign In
3. Register (Urdu)
4. Sign In (Urdu)
5. Track Your Symptoms
6. Medication Manager
7. Exercise & Therapy
8. Brain Games


Horizontal Flows:
* Download button under:
* Track Your Symptoms → Symptom History
* Medication Manager → Track Medicines
* Settings
* Profile
* Accessibility Settings (Redirects to in-built phone settings; supports both English and Urdu)




Flow and Navigation:
* Back Icon: Will take you back to the previous page
* Home Icon: Will take you directly to the home screen, from wherever you are in the app


Start Up Page:
Un-clickable:
* Settings: Will open your Android/IOS settings and take u to where you can turn on Accessibility settings
Clickable:
* Skip : close popup and show the main landing page
* Register: Take you to Create an Account
* Sign In: Take you to Sign In




Create an Account (Page 1):
Un-clickable:
* Full Name field
* DOB
* Date of Diagnosis
* Country
Clickable:
* Cancel: go back.
* Next: next page of create account.


(Page 2):
Un-clickable:
* Phone Number
* Password
* Checkboxes
* Read Here
* Unhide password
Clickable:
* Back: Go back.
* Next: Finish. (Will show you error messages the first time you click it.)
* Clicking Next again will take you the main Home screen (after showing a loading screen)


Sign In:
Un-clickable: 
* Phone Number
* Password 
* CheckBox 
* Forgot Password
* Unhide password
Clickable:
* Sign In: redirects to the main Home screen (after showing a loading screen)


Home Screen:
Clickable:
* Settings icon (top-left) will take you to the Settings screen
* Profile icon (top-right) will take you to the Profile Screen
* Track Your Symptoms
* Medication Manager
* Exercise & Therapy
* Brain Games
Will take you to the main screen for each feature
The ‘Upcoming Reminders’ screen is not clickable, it is only supposed to show the nearest upcoming medication reminder.




Profile: 
View your account details.


Clickable:
* Edit: will take you to the Edit Profile screen, where you can edit all account details


Edit Profile: 
Un-clickable:
* All editable fields
Clickable:
* Cancel will take you back to view Profile, discarding changes
* Save is supposed to update your Profile details.


In the Prototype, both do the same thing.


Settings:
Clickable: 
* Sign out: Shows a pop-up.
* Pressing Cancel on the pop-up will return you to the settings screen
* Sign Out will take you to the landing page, where you can choose to register or login




Track Your Symptoms:
Clickable: 
* Log Your Symptoms. 
* Symptom History.


1. Log Your Symptoms:
* Clicking on View or edit the symptoms for the specified day (today or yesterday).
* If you click edit or view it shows you the No Symptoms Added screen, you can click on Add.
* This takes you to the symptom logger where you can click on the rating scales and continue. Only next, back and home buttons are clickable.
* If you click the ‘view’ button on yesterday’s log, it takes you to the view screen from where you can view symptoms or go back.


2. Symptom History 
* It takes you to the symptom history calendar where only the date 12 is clickable.
* Clicking on date 12 shows the symptom log from that day.
* Charts and download are also clickable.
* Clicking Chart shows the charts and the screen is scrollable.
* Clicking Download shows a popup, comprising of two buttons Yes or No which are clickable. No does nothing. Yes gives the notification of downloaded.












Medication Manager
Clickable:
* Create Medicine Schedule: Will take you to add medicine
* View/Edit Schedule: Will take you to Medicine Schedule
* Track Medicines: Will take you to Track Medicines


1. Add Medicine:
Only follow this flow:
* Click the plus to increase the Frequency to 2.
* Click Done.
* You will be taken to the Medicine Schedule .
* Click Edit.
* Click Add.
* Click Add Med.
* Click Done.
You will be taken to the Medicine Schedule.


2. View/Edit Schedule:
You will start at Medicine Schedule, where you view your schedule.
* Click Edit: Will take you to edit Schedule.
* Delete Centrum (You can cancel or delete).
Once you have deleted Centrum.
* Edit Levadopa.
* Just click Done (other fields are not interactable).
Done will take you back.
* Click on Add Med.
* Click on Done.
You will be taken to the Medicine Schedule.


3. Track Medicines:
* Click on Download Monthly Report.
* Confirm by either clicking Yes or No on the popup.
If yes is clicked, notification will be shown to show the downloaded file.




Exercise & Therapy:
Clickable:
* Tandem Walking.
* Wrist Rotations.
* Category buttons: will take you to appropriate screens.


1. Therapy Category Screens:
Display videos for each category.
* Flexibility & Strength (contains a clickable video)
* Balance & Gait (contains a clickable video)
* Coordination
* Breathing & Voice Therapy


2. Recommended Screens:
* Clicking on Tandem Walking or Wrist Rotations redirects to an in-app video player.


3. In-app video player:
* Clicking on full screen icon takes you to full screen mode.


4. Full screen player:
* Clicking on normal screen icon takes you back to the previous screen.
* Minimize icon does the same.




Brain Games:
Clickable:
* 4 games.
* Back and Home Buttons.


1. When a user selects a game from the Brain Games main screen:
1. They are first taken to an Instructions Screen, which outlines how to play.
2. After reading the instructions, the user taps the "Play" button.
3. This navigates to a Game Screen, which visually simulates what gameplay would look like.
4. The back button takes the user to the main brain games page.
2. Back Button:
* Redirects to main Brain Games screen.
3. Home Button:
* Redirects to main Home screen.


Note: These game screens are mock-ups only. The actual games are not playable in this prototype. Only the UI and feedback visuals (score, high score, layout) have been designed.