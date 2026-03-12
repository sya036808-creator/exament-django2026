import os
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        # Fichier de log pour les messages (facile à lire dans VS Code)
        log_file = os.path.join(settings.BASE_DIR, 'messages_recus.txt')
        
        # On intercepte l'email de réinitialisation de mot de passe
        if template_prefix == 'account/email/password_reset_key':
            user = context.get('user')
            reset_url = context.get('password_reset_url')
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("\n" + "="*60 + "\n")
                # Si l'utilisateur possède un numéro de téléphone, on simule l'envoi d'un SMS
                if user and hasattr(user, 'phone_number') and user.phone_number:
                    sms_text = (
                        f"📱 SMS ENVOYÉ AU : {user.phone_number}\n"
                        f"MESSAGE : Bonjour {user.first_name or user.username}, voici votre lien pour "
                        f"réinitialiser votre mot de passe : {reset_url}\n"
                    )
                    f.write(sms_text)
                    print(sms_text) # Aussi dans la console
                else:
                    email_text = (
                        f"📧 EMAIL ENVOYÉ À : {email}\n"
                        f"MESSAGE : Bonjour, voici votre lien pour réinitialiser "
                        f"votre mot de passe : {reset_url}\n"
                    )
                    f.write(email_text)
                    print(email_text)
                f.write("="*60 + "\n")
        
        # Par défaut on laisse allauth envoyer l'email normalement
        return super().send_mail(template_prefix, email, context)
