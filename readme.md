### Kindle Sender
Simple TKinter app that can send files to your kindle email address.

#### Usage
1. Get your kindle email. [how?](https://www.amazon.com/sendtokindle/email)
2. Create a .env file in the same directory as the .py with contents like below
```env
MAIL_HOST=your_smtp_host
MAIL_USER=amazon_approved_email
MAIL_APP_PASSWORD=email_password
```
Notes:
- Your smtp host will depend on your email provider, for example gmail is `smtp.gmail.com`.
- Your amazon approved email is the email you used to register your kindle, or any other added to your approved list.
- You almost certainly can't use your regular email password, you'll need to generate an app password from your email provider. [example for gmail](https://support.google.com/accounts/answer/185833?hl=en)
- YOU MUSN'T SHARE YOUR .ENV FILE WITH ANYONE!
- You can also set
```env
DEFAULT_DESTINATION_USER=your_kindle_email
```
to avoid having to paste your kindle email every time you run the app.

3. Run the .py file, browse for the file you want to send, paste your kindle email, and click send.

#### Problems
- I use simple deUTF8 to avoid encoding problems, but it's not perfect. You can rename problematic book by hand if needed, or fix the code.
- App doesn't report progress, so you'll have to wait until it's done. (It can take a while for big or many files.)

#### TODOs
- [ ] Add progress bar/window
- [ ] Improve file list / file removal
