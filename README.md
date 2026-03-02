## Hvorfor Flat File?

En flat file database gemmer data direkte i en JSON-fil.
- Dette kan være smart fordi
- Ingen database server kræves
- Filen er human-readable
- Let at flytte og backe op




REST API
<img width="1687" height="1284" alt="image" src="https://github.com/user-attachments/assets/0658a058-b01e-42f7-85df-d8311af3a5b5" />


## Encrypting
Jeg valgte AES-256 til at kryptere PII fordi det er industri standarden

## When should data be encrypted?
Data shouyld be encrypted when they get saved, as in before they get written to the JSON-file.
PII like name and adress are sensetive and may not be saved as plaintext

## when should data be decrypted?
Data should only be decrypted when they need to be used.

##When should decrypted data be removed from memory?
ASAP and overwirte it with x00 where possible.

## Should you pay attention to anything else?
 **GDPR**: PII NEEDS to be protected.
 - **Keyhandling** The AES key should not be hardcoded in production.
 - **Hashing**: Use bcrypt/argon2 istead of SHA-256 in actual prod. 

Encryption
<img width="675" height="584" alt="image" src="https://github.com/user-attachments/assets/932743e1-4e8f-49a8-bba9-92c6ca0bc459" />



## Hashinng
I chose SHA-256 to passwords as they may never be stored in plaintext.
Hashing is oneway, you cannot figure out the password from a hash.
<img width="785" height="242" alt="image" src="https://github.com/user-attachments/assets/d89c3d21-4a63-4f7c-b62c-8faae87eeb0c" />



Encrypted user information
<img width="1161" height="250" alt="image" src="https://github.com/user-attachments/assets/f32d8531-54f7-43c9-bbb9-453df704895e" />


Bearer token
<img width="1535" height="767" alt="image" src="https://github.com/user-attachments/assets/aab7d2f8-3187-4165-9be0-8aa6f0c7f447" />


Endpoint usage of token
<img width="1552" height="1287" alt="image" src="https://github.com/user-attachments/assets/7bf45262-aa41-401a-97fb-184effd821e5" />


## UNIT test
Ricisi hvis test fejler
- **test_create_and_find_user fejler**: Brugere kan ikke oprettes eller hentes — systemet er ubrugeligt
- **test_data_persists_after_reload fejler**: Al data går tabt ved genstart — kritisk produktionsfejl
- **test_disable_enable_user fejler**: Deaktiverede brugere kan stadig logge ind
- **test_update_first_name fejler**: Opdatering af brugerdata virker ikke
- **test_get_user_that_does_not_exist fejler**: Systemet crasher ved ugyldige opslag



Passed Tests
<img width="711" height="709" alt="image" src="https://github.com/user-attachments/assets/f1970233-1d08-4f3b-a105-8c4e8d951c40" />
