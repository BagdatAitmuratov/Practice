/*1_EXE*/
CREATE OR REPLACE FUNCTION find_name_or_phone(phbok text)
RETURNS TABLE(p_name VARCHAR,p_phone VARCHAR) as $$
BEGIN
    RETURN QUERY
    SELECT pb.name,pb.phone
    FROM phonebook_pr8 pb
    WHERE pb.name ILIKE '%' ||phbok|| '%'
    OR pb.phone ILIKE '%' ||phbok|| '%';
END;
$$ LANGUAGE plpgsql;
/*3-exe*/
CREATE OR REPLACE FUNCTION insert_many_users(names_arr text[],phones_arr text[])
RETURNS TABLE(enter_name text,enter_phone text) as $$
DECLARE 
    i INTEGER
BEGIN
    for i in 1.array_length(names_arr,1) LOOP
        IF length(phones_arr[i])=11 and phones_arr[i] ~ '^[0-9]$' then 
            insert into phonebook_pr8 (name, phone) 
            values (names_arr[i], phones_arr[i])
        ELSE
            err_name := names_arr[i];
            err_phone := phones_arr[i];
            RETURN NEXT;
        END IF;
        
    END LOOP;
END;
$$ LANGUAGE plpgsql;
/*4_exe*/
CREATE OR REPLACE FUNCTION get_contact_pages(p_limit INT,p_offset INT)
RETURNS TABLE (name VARCHAR,phone VARCHAR) AS $$
BEGIN 
    RETURN QUERY
    SELECT phb.name,phb.phone FROM phonebook_pr8 phb
    ORDER BY phb.name LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

