from pprint import pformat

import FIXME
import SKIPPED


def for_all_elements(elements, foo):
    def for_all_wrapper(func):
        def wrapper(self):

            used = {}
            for i in elements:
                try:
                    name = foo(i)
                    func(self, i)
                except AssertionError as msg:
                    used[name] = [name, msg]
            excluded = set()
            if hasattr(SKIPPED, func.__name__ + "_SKIPPED"):
                excluded = excluded.union(getattr(SKIPPED, func.__name__ + "_SKIPPED"))
            if hasattr(FIXME, func.__name__ + "_FIXME"):
                excluded = excluded.union(getattr(FIXME, func.__name__ + "_FIXME"))

            to_delete = {element for element in excluded if element in used}
            
            for i in to_delete:
                used.pop(i)
                excluded.remove(i)

            errors_verbose = ""            
            for i in used:
                name = used[i][0]
                msg = used[i][1]
                errors_verbose += "\nError in element " + pformat(name) + ": " + str(msg)
            

            errors = {used[i][0] for i in used}
            msg_errors = "\nErrors in files:\n" + pformat(errors) + "\n\n" + errors_verbose
            msg_excluded = "\nNo errors detected in elements:\n" + pformat(excluded) + "\nbut the elements were excluded in FIXME.py or SKIPPED.py file."

            # if len(used) > 0 or len(excluded) > 0:
            #     print()
            #     print("Errors: ", errors)
            #     print("Excluded: ", excluded)
            
            # if len(errors) > 0 and len(excluded) > 0:
            #     self.fail(msg_errors + "\n" + msg_excluded)

            # if len(errors) > 0:
            #     self.fail(msg_errors)
            
            # if len(excluded) > 0:
            #     self.fail(msg_excluded)

        return wrapper

    return for_all_wrapper
