#  External
from datetime import datetime
import multiprocessing

# doenv
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), ".env"))

# Internal
import outils
import function


def main():
    if __name__ == "__main__":
        start = datetime.now()
        env = input("Quel est l'environnement a utiliser ? prod, dev(defaut), local : ")
        if not env:
            env = "dev"
        store_selected = input("Quel est le store ciblé (un a la fois)? : ")
        if not store_selected:
            print("Vous devez choisir un store.")
        # TODO: input for nb_part
        nb_part = 4

        stores = function.get_store_to_parse(env, store_selected)
        for store in stores:
            treated = function.get_treated_elements(env, store)
            if len(treated) != 0:
                del treated[0]
            uri = function.get_uri_from_store(env, store, treated)
            tabs_uri = function.split_array_equally(uri, nb_part)

            # Initialiser les queues
            multiprocessingMonitor = multiprocessing.Queue()
            processus = []
            try:
                for i in range(nb_part):
                    if len(tabs_uri) > 0:
                        p = multiprocessing.Process(
                            target=outils.worker, args=(env, store, i, tabs_uri[i])
                        )
                        processus.append(p)
                        p.start()
                    else:
                        print("[ERREUR] Pas de URI à traiter")
                print("[INFO] Tous les processus ont terminé.")

            except Exception as e:
                print(f"Une erreur s'est produite : {e}")

            finally:
                for p in processus:
                    p.join()

                end = datetime.now()
                print("[TEMPS] Time spent", end - start)


main()
