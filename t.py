import threading
import queue


def calcola_risultato(stop_event):
	stop_event.set()
	return 10

def funzione_lenta(stop_event, queue):
    result = None
    while not stop_event.is_set():
        # codice della funzione
        # ...
        result = calcola_risultato(stop_event)
    queue.put(result)

# crea una coda per passare il risultato della funzione lenta al thread principale
queue = queue.Queue()

# crea un evento di stop
stop_event = threading.Event()

# crea un thread per eseguire la funzione_lenta
thread = threading.Thread(target=funzione_lenta, args=(stop_event, queue))

# avvia il thread
thread.start()

# attendi per un massimo di 5 secondi prima di interrompere il thread
thread.join(5)

# se il thread è ancora in esecuzione, imposta l'evento di stop
if thread.is_alive():
    print("La funzione sta impiegando troppo tempo, interrompendo...")
    stop_event.set()

# attendi che il thread termini l'esecuzione
thread.join()

# ottieni il risultato della funzione lenta dalla coda
result = queue.get()
print(result)
# esegui un'altra funzione utilizzando il risultato ottenuto
altra_funzione(result)

#In questo modo, la funzione lenta viene eseguita in un thread separato e il suo risultato viene passato al thread principale utilizzando una coda. Una volta che il thread viene interrotto, il risultato viene inserito nella coda e può quindi essere recuperato dal thread principale.

