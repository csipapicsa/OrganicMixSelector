from multiprocessing import Process, Queue
import functions as f
import time

def split_dataframe(df, n_splits):
    """Split a DataFrame into roughly equal parts."""
    split_size = len(df) // n_splits
    return [df.iloc[i:i + split_size] for i in range(0, len(df), split_size)]

def fast_comparisson_splitted(queue, df_seqment, df):
    df_list = df.values.tolist()
    df_list_inside = df_seqment.values.tolist()
    edge_list_to_list = []
    for row_base in df_list:
        for row_to_compare in df_list_inside:
            if row_base[0] == row_to_compare[0]:
                None
            else:
                # first filter, song is whennever between ranges? 
                if row_base[7] >= row_to_compare[6] and row_base[8] <= row_to_compare[6]:
                    # only a temporary function:
                    if row_base[9] == row_to_compare[9]:
                        edge_list_to_list.append((row_base[0], row_to_compare[0]))
                    else:
                        None
                    if row_to_compare[12] in f.get_classic_neighbours(row_base[12]):    
                        #print(row_base.ID, row_to_compare.ID)
                        edge_list_to_list.append((row_base[0], row_to_compare[0]))
                    else:
                        None
                else:
                    None
    queue.put(edge_list_to_list)

def parallel_job(df, cores=8):
    df_segments = split_dataframe(df, cores)
    processes = []
    queue = Queue()

    for segment in df_segments:
        # Pass the queue as the first argument to the target function
        process = Process(target=fast_comparisson_splitted, args=(queue, segment, df))
        processes.append(process)
        process.start()

    results = []
    for _ in range(len(processes)):
        # Retrieve results from the queue
        results.extend(queue.get())  # Use extend to flatten the list of lists

    for process in processes:
        process.join()

    # 'results' now contains all the edges from all processes
    return results
 