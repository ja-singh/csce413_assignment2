# Honeypot Analysis

## Summary of Observed Attacks
Attacks using tools like `netcat` were captured in full, showing that the honeypot accurately logs raw string input and manual interaction. Attacks using protcols like SSH were not fully decrypted; however, there were still identifable information that could be extracted from them (such as lient banners, key encryption algorithms, etc.).
While many of my own simulated attacks were logged, there was an instance of a logged automated attack from the IP address `172.20.0.1`.

## Notable Patterns
- Common key encryption algotihms used by the automated attacks were `aes256-gcm` and `chacha20-poly1305`.
- While obvious, the manual attacks range for longer periods of time (15 - 30 seconds) while the automated attack last a very short duration of only 0.001 seconds. 

## Recommendations
To further improve this honeypot, I would:
- Move towards more complex implementations of a honeypot. While a complete high-interaction honeypot may be a bit unnecessary for this assignment, I could use libraries like `paramiko` that support SSH to better aquire the data from intruders attempting to connect via SSH.
- Specific Alerts: As of now, the log simply records when any intrusion is made. The honeypot could be more useful or procide greater indication of the severity of the intrusion if it specifically flagged when a user attemped to login as admin, when a specific password was tried, etc. 