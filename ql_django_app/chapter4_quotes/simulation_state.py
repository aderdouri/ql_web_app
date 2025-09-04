# chapter4_quotes/simulation_state.py

# Ce module agira comme une mémoire vive persistante pour nos objets QuantLib.
# Il est initialisé une seule fois au démarrage du serveur et partagé entre toutes les requêtes.
SHARED_QL_OBJECTS = {}