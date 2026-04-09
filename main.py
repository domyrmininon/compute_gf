import time
import artin
import word_class
import json

"""
#Personnalize coxeter matrix
coxeter_matrix = np.array([
    [1, 2],
    [2, 1]
])
"""

runs = {
    "C_2_affine": artin.get_coxeter_matrix_of_type_C_affine(3), # n generators means type C affine of rank n-1
    "C_3_affine": artin.get_coxeter_matrix_of_type_C_affine(4), # n generators means type C affine of rank n-1
    "G_2_affine": artin.get_coxeter_matrix_of_type_G_affine(3), # Type G affine of rank 2
    "B_3_affine": artin.get_coxeter_matrix_of_type_B_affine(4), # n generators means type B affine of rank n-1
    "A_4": artin.get_coxeter_matrix_of_type_A(4),
    "F_4": artin.get_coxeter_matrix_of_type_F(4),
    "A_3_affine": artin.get_coxeter_matrix_of_type_A_affine(4), # n generators means type A affine of rank n-1
    "A_4_affine": artin.get_coxeter_matrix_of_type_A_affine(5), # n generators means type A affine of rank n-1
    "D_4_affine": artin.get_coxeter_matrix_of_type_D_affine(5), # n generators means type D affine of rank n-1
}

def get_garside_family(coxeter_matrix):
    n = coxeter_matrix.shape[0]
    rc = artin.rc_from_coxeter_matrix(coxeter_matrix)
    total_time = time.time()
    gf = word_class.compute_garside_family(rc, n)
    gf = sorted(gf, key=lambda x: len(x.l))
    print("\nGarside family has size", len(gf))
    print(f"Total time: {time.time() - total_time:.2f} seconds")
    return gf


for name, coxeter_matrix in runs.items():
    file_name = f"results/garside_family_{name}.py"
    #check if the file already exists, if it does, skip the computation
    try:        
        with open(file_name, "r") as f:
            print(f"Garside family for {name} already computed, (delete file to recompute) skipping...")
    except FileNotFoundError:
        print(f"\nComputing Garside family for {name}...")
        gf = get_garside_family(coxeter_matrix)
        gf_str = [str(w) for w in gf]
        with open(file_name, "w") as f:
            json.dump(gf_str, f)
        #write in resulte summary file
        with open("results/summary.txt", "a") as f:
            f.write(f"{name}: size of Garside family = {len(gf)}\n")
