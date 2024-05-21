#  External
from datetime import datetime
import multiprocessing
import argparse

parser = argparse.ArgumentParser(
    description="Scanner de produits simple Magento pour les images transparente, les produits 3 colonnes, les pages 404."
)
parser.add_argument(
    "--env",
    type=str,
    default="dev",
    help="L'environement à utiliser (ex: prod) [prod, dev, local]",
)
parser.add_argument(
    "--stores", type=str, help="Quels stores sont à scanner (ex:  1, 5, 8)"
)
parser.add_argument(
    "--nb_processing",
    type=int,
    default=4,
    nargs="?",
    help="Quels est le nombre de process (ex: 4)",
)
args = parser.parse_args()

# doenv
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), ".env"))

# Internal
import outils
import function


def main():
    if __name__ == "__main__":
        env = args.env
        store_selected = args.stores
        nb_part = args.nb_processing

        start = datetime.now()
        stores = function.get_store_to_parse(env, store_selected)
        for store in stores:
            treated = function.get_treated_elements(env, store)
            if len(treated) != 0:
                del treated[0]
            uri = function.get_uri_from_store(env, store, treated)
            tabs_uri = function.split_array_equally(uri, nb_part)

            # Initialiser les queues
            multiprocessing.Queue()
            processus = []
            try:
                for i in range(nb_part):
                    if len(tabs_uri) > 0 and len(tabs_uri[i]) > 0:
                        p = multiprocessing.Process(
                            target=outils.worker, args=(env, store, i, tabs_uri[i])
                        )
                        processus.append(p)
                        p.start()
                    else:
                        print("[INFO] Pas de URI à traiter")
                print("[INFO] Tous les processus ont terminé.")

            except Exception as e:
                print(f"Une erreur s'est produite : {e}")

            finally:
                for p in processus:
                    p.join()

                end = datetime.now()
                print("[TEMPS] Time spent", end - start)


main()
