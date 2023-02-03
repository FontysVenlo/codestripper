package phonebook;
//cs:remove:start
import static java.lang.String.format;
import java.util.HashMap;
import java.util.Map;
//cs:remove:end

/**
 * PhoneBook class to manage contacts.
 * @author urs//cs:replace:* @author test
 */
public class Phonebook {

    //cs:uncomment:start
    //Test
    //Should uncomment this
    //cs:uncomment:end

    //cs:remove:start
    private final Map<String, BookEntry> book;
    //cs:remove:end
    //cs:add://TODO add field(s)

    /**
     * Initializes your phone book.
     */
    public Phonebook() {
        //cs:add://TODO
        book = new HashMap<>();//cs:remove
    }

    /**
     * Adds entry to your phone book. If an entry with this name already exists,
     * just an additional phone number is added.
     * @param name of a relative person
     * @param number belonging to the name.
     */
    public void addEntry(String name, String number) {
        //Start Solution::replacewith:://TODO
        //book.computeIfAbsent(name, (s) -> new BookEntry(s, number));

        BookEntry existingEntry = book.get( name );

        if ( existingEntry != null ) {
            existingEntry.addNumber(number);
        } else {
            book.put( name, new BookEntry( name, number ) );
        }
        //End Solution::replacewith::
    }

    /**
     * Search your phone book by name and return all information about the person
     * with this name as text.
     * @param name to lookup
     * @return all info about this person, or null if not found
     */
    public String searchByName(String name) {
        //Start Solution::replacewith:://TODO
        String result = null;
        BookEntry entry = book.get(name);
        if (entry != null) {
            result = format("%s has number %s and address %s", name, entry.getAddress(), entry.getNumber());
        }
        return result;
        //End Solution::replacewith::return null;
        //cs:add:return null
    }

    /**
     * Search all information belonging to a person with the given phone number.
     * @param number to search
     * @return all info about the belonging person, or null if not found.
     */
    public String searchByNumber(String number) {
        //Start Solution::replacewith:://TODO
        for (Map.Entry<String, BookEntry> entry : book.entrySet()) {
            if (entry.getValue().hasNumber(number)) {
                return entry.toString();
            }
        }
        return null;

        //End Solution::replacewith::return null;
    }

    /**
     * Add address to name. Adds a new address if there is no address yet, otherwise
     * the address is updated.
     * @param name to add address to
     * @param address address to add
     */
    public void addAddress(String name, String address) {
        //Start Solution::replacewith:://TODO
        book.get(name).setAddress(address);
        //End Solution::replacewith::
    }

    /**
     * Delete entry from phone book.
     * @param name whose entry should be deleted.
     */
    public void deleteEntry(String name) {
        //Start Solution::replacewith:://TODO
        book.remove(name);
        //End Solution::replacewith::
    }
}