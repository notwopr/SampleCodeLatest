# TAKES TWO LISTS AND RETURNS LIST OF THE TOP X ITEMS BY CRITERIA OF SECOND LIST
def topgun(list1, list2):

    combinedlist = [[list1[i], list2[i]] for i in range(0, len(list1))]

    df = pd.DataFrame(
        data=combinedlist,
        columns=[
            "TICKER",
            "SLOPE"
        ]
    )

    # SORT RESULTS
    df.sort_values('SLOPE', axis=0, ascending=False, inplace=True)

    return df



# RETURN LIST OF TWO VARIABLE WEIGHTS GIVEN CONSTRAINTS
def two_var_weights(var1_list, var2_list, var1key, var2key):

    all_candidates = []
    all_vars = [var1_list, var2_list]
    all_keys = [var1key, var2key]

    # FOR EACH VARIABLE...
    for (varlist, chosenkey) in zip(all_vars, all_keys):

        # MAKE EDITABLE COPY
        varlist_copy = all_vars.copy()
        keylist_copy = all_keys.copy()

        # REMOVE CHOSEN VARLIST ...
        varlist_copy.remove(varlist)
        keylist_copy.remove(chosenkey)

        # FOR EVERY WEIGHT IN CHOSEN VARLIST...
        for w_elem in varlist:

            secondkey = keylist_copy[0]
            weight_set = [{chosenkey: round(w_elem, 2), secondkey: round(1 - w_elem, 2)}]
            all_candidates.extend(weight_set)

    # BUILD REJECTION LIST
    rejected_list = []
    for candidate in all_candidates:

        for (varlist, selectkey) in zip(all_vars, all_keys):

            # DEFINE BOUNDS
            maxvarval = np.max(varlist)
            minvarval = np.min(varlist)

            # IF OUTSIDE BOUNDS ADD TO REJECTION LIST
            if minvarval > candidate[selectkey] or candidate[selectkey] > maxvarval:
                rejected_list.append(candidate)

    # BUILD PASSED CANDIDATES LIST
    prelim_weight_list = []
    for candidate in all_candidates:
        if candidate not in rejected_list:
            prelim_weight_list.append(candidate)

    # REMOVE DUPES
    final_weight_list = removedupes_lists('', prelim_weight_list)

    return final_weight_list


# RETURN LIST OF THREE VARIABLE combinations
def three_var_combinations(var1_list, var2_list, var3_list, var1key, var2key, var3key):

    all_var_combos = []
    for var1option in var1_list:

        for var2option in var2_list:

            for var3option in var3_list:
                optionset = {var1key: var1option, var2key: var2option, var3key: var3option}
                all_var_combos.append(optionset)

    return all_var_combos


# RETURN LIST OF THREE VARIABLE WEIGHTS GIVEN CONSTRAINTS
def three_var_weights(var1_list, var2_list, var3_list, var1key, var2key, var3key):

    all_candidates = []
    all_vars = [var1_list, var2_list, var3_list]
    all_keys = [var1key, var2key, var3key]

    # FOR EACH VARIABLE...
    for (varlist, chosenkey) in zip(all_vars, all_keys):

        # MAKE EDITABLE COPY
        varlist_copy = all_vars.copy()
        keylist_copy = all_keys.copy()

        # REMOVE CHOSEN VARLIST ...
        varlist_copy.remove(varlist)
        keylist_copy.remove(chosenkey)

        # FOR EVERY WEIGHT IN CHOSEN VARLIST...
        for w_elem in varlist:

            # FOR EACH REMAINING VARIABLE...
            for (remlist, secondkey) in zip(varlist_copy, keylist_copy):

                # ASSIGN LAST REMAINING KEY
                lastkeylist = keylist_copy.copy()
                lastkeylist.remove(secondkey)
                lastkey = lastkeylist[0]

                weight_set = [{chosenkey: round(w_elem, 2), secondkey: round(item, 2), lastkey: round(1 - item - w_elem, 2)} for item in remlist]
                all_candidates.extend(weight_set)

    # BUILD REJECTION LIST
    rejected_list = []
    for candidate in all_candidates:

        for (varlist, selectkey) in zip(all_vars, all_keys):

            # DEFINE BOUNDS
            maxvarval = np.max(varlist)
            minvarval = np.min(varlist)

            # IF OUTSIDE BOUNDS ADD TO REJECTION LIST
            if minvarval > candidate[selectkey] or candidate[selectkey] > maxvarval:
                rejected_list.append(candidate)

    # BUILD PASSED CANDIDATES LIST
    prelim_weight_list = []
    for candidate in all_candidates:
        if candidate not in rejected_list:
            prelim_weight_list.append(candidate)

    # REMOVE DUPES
    final_weight_list = removedupes_lists('', prelim_weight_list)

    return final_weight_list


# RETURN LIST OF FOUR VARIABLE WEIGHTS GIVEN CONSTRAINTS
def four_var_weights(var1_list, var2_list, var3_list, var4_list, var1key, var2key, var3key, var4key):

    all_candidates = []
    all_vars = [var1_list, var2_list, var3_list, var4_list]
    all_keys = [var1key, var2key, var3key, var4key]

    # FOR EACH KEY...
    for (firstvarlist, firstkey) in zip(all_vars, all_keys):

        # MAKE EDITABLE COPY
        all_vars_minus1 = all_vars.copy()
        all_keys_minus1 = all_keys.copy()

        # REMOVE FIRST CHOSEN KEY ...
        all_vars_minus1.remove(firstvarlist)
        all_keys_minus1.remove(firstkey)

        # FOR EVERY WEIGHT IN FIRST KEY...
        for fvl_elem in firstvarlist:

            # CHOOSE SECOND KEY ...
            for (secondvarlist, secondkey) in zip(all_vars_minus1, all_keys_minus1):

                # MAKE EDITABLE COPY
                all_vars_minus2 = all_vars_minus1.copy()
                all_keys_minus2 = all_keys_minus1.copy()

                # REMOVE SECOND CHOSEN VARLIST ...
                all_vars_minus2.remove(secondvarlist)
                all_keys_minus2.remove(secondkey)

                # FOR EVERY WEIGHT IN SECOND CHOSEN KEY...
                for svl_elem in secondvarlist:

                    # FOR EACH REMAINING KEY...
                    for (remlist, thirdkey) in zip(all_vars_minus2, all_keys_minus2):

                        # ASSIGN LAST REMAINING KEY
                        lastkeylist = all_keys_minus2.copy()
                        lastkeylist.remove(thirdkey)
                        lastkey = lastkeylist[0]

                        weight_set = [{firstkey: round(fvl_elem, 2), secondkey: round(svl_elem, 2), thirdkey: round(item, 2), lastkey: round(1 - item - fvl_elem - svl_elem, 2)} for item in remlist]
                        all_candidates.extend(weight_set)

    # BUILD REJECTION LIST
    rejected_list = []
    for candidate in all_candidates:

        for (varlist, selectkey) in zip(all_vars, all_keys):

            # DEFINE BOUNDS
            maxvarval = np.max(varlist)
            minvarval = np.min(varlist)

            # IF OUTSIDE BOUNDS ADD TO REJECTION LIST
            if minvarval > candidate[selectkey] or candidate[selectkey] > maxvarval:
                rejected_list.append(candidate)

    # BUILD PASSED CANDIDATES LIST
    prelim_weight_list = []
    for candidate in all_candidates:
        if candidate not in rejected_list:
            prelim_weight_list.append(candidate)

    # REMOVE DUPES
    final_weight_list = removedupes_lists('', prelim_weight_list)

    return final_weight_list
