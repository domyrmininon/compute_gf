import time
import artin
from compute_garside import get_garside_family
import word_class
import json


runs = {
    "A_4": artin.get_coxeter_matrix_of_type_A(4),
    "F_4": artin.get_coxeter_matrix_of_type_F(4),
    "C_2_affine": artin.get_coxeter_matrix_of_type_C_affine(3), # n generators means type C affine of rank n-1
    "C_3_affine": artin.get_coxeter_matrix_of_type_C_affine(4), # n generators means type C affine of rank n-1
    "G_2_affine": artin.get_coxeter_matrix_of_type_G_affine(3), # Type G affine of rank 2
    "B_3_affine": artin.get_coxeter_matrix_of_type_B_affine(4), # n generators means type B affine of rank n-1
    "A_3_affine": artin.get_coxeter_matrix_of_type_A_affine(4), # n generators means type A affine of rank n-1
    "A_4_affine": artin.get_coxeter_matrix_of_type_A_affine(5), # n generators means type A affine of rank n-1
    "D_4_affine": artin.get_coxeter_matrix_of_type_D_affine(5), # n generators means type D affine of rank n-1
}

def is_right_divisor(u, v, rr_table, rc):
    # Check if u is a right divisor of v
    if len(u) > len(v):
        return False
    v_rev = v[::-1]
    u_rev = u[::-1]
    try:
        _, up = word_class.right_complement_check_loop(u_rev, v_rev, rc = rc, rr_table=rr_table)
    except:
        return False
    return up.l == [] 

def get_extremal_elements(coxeter_matrix, garside_family):
    extremal_elements = []
    rr_table = {}
    rc = artin.rc_from_coxeter_matrix(coxeter_matrix)
    for w in garside_family[::-1]: # We start with the longest elements
        for e in extremal_elements:
            if is_right_divisor(w, e, rr_table, rc):
                break
        else: # if we didn't break, it means w is not a right divisor of any element in extremal_elements, so we add it to the list
            extremal_elements.append(w)
    return extremal_elements
        

for name, coxeter_matrix in runs.items():
    file_name = f"results/garside_family_{name}.py"
    output_file_name = f"results/extremal_elements_{name}.py"
    #check if the file already exists, if it does, skip the computation
    try:        
        with open(file_name, "r") as f:
            try:
                with open(output_file_name, "r") as f:
                    print(f"Extremal elements for {name} already computed")
                    continue
            except FileNotFoundError:
                pass
            print(f"Garside family for {name} found")    
            gf = json.load(f)
            extremal_elements = get_extremal_elements(coxeter_matrix, gf)
            with open(output_file_name, "w") as f:
                json.dump([str(w) for w in extremal_elements], f)
            #write in summary file
            with open("results/summary.txt", "a") as f:
                f.write(f"{name}: number of extremal elements = {len(extremal_elements)}\n")

    except FileNotFoundError:
        print(f"No Garside family for {name} found")