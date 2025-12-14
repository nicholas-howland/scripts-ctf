# THM TakeOver Room Writeup

## Objective
Hello there,

I am the CEO and one of the co-founders of futurevera.thm. In Futurevera, we believe that the future is in space. We do a lot of space research and write blogs about it. We used to help students with space questions, but we are rebuilding our support.

Recently blackhat hackers approached us saying they could takeover and are asking us for a big ransom. Please help us to find what they can takeover.

Our website is located at https://futurevera.thm

Hint: Don't forget to add the MACHINE_IP in /etc/hosts for futurevera.thm ; )
## Target
10.10.14.61

## Steps Taken
- Accessed site via https and looked at the self signed certificate
- Tried subdomain of support.futurevera.thm and was lead to the support site who's certificate had a custom domain name stored in the certificate.
- Added the custom domain name for to the hosts file and accessed the site on port 80 and was presented with a flag in the url.

# Additional Information
- Had nothing to do with DNS
