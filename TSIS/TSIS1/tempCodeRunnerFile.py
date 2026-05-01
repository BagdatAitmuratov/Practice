
        elif choice == '4': export_to_json(conn)
        elif choice == '5': import_from_json(conn)
        elif choice == '6': call_procedure_add_phone(conn)
        elif choice == '7': call_procedure_move_to_group(conn)
        elif choice == '8': call_function_search_contacts(conn)
        elif choice == '9': import_from_csv(conn)
        elif choice == '0':
            print("Exiting PhoneBook. Goodbye!")