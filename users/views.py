from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

# Vue pour la mise à jour du profil utilisateur
# Le décorateur @login_required assure que seul un utilisateur connecté peut y accéder
@login_required
def profile_update(request):
    # Si la requête est de type POST, cela signifie que le formulaire a été soumis
    if request.method == 'POST':
        # On remplit le formulaire avec les données soumises et les fichiers (pour l'avatar)
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        # Si les données du formulaire sont valides
        if form.is_valid():
            # On enregistre les modifications dans la base de données
            form.save()
            # On affiche un message de succès
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            # On redirige vers la même page pour éviter la double soumission
            return redirect('profile_update')
    else:
        # Si la requête est de type GET, on affiche un formulaire pré-rempli avec les infos de l'utilisateur
        form = UserProfileForm(instance=request.user)
    
    # On rend le template profile.html en lui passant le formulaire
    return render(request, 'users/profile.html', {'form': form})
