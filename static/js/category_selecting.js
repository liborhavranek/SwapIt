$(document).ready(function() {
    // Funkce pro načtení podkategorií
    function loadSubcategories(categoryId, container) {
        $.ajax({
            url: `/get_subcategories/${categoryId}`,
            method: 'GET',
            success: function(response) {
                const subcategories = response.subcategories;
                if (subcategories.length > 0) {
                    // Vytvoření nového select elementu pro podkategorie
                    const newSelect = $('<select>')
                        .addClass('form-select category-select mt-3')
                        .attr('name', 'selected_category')
                        .append('<option value="" disabled selected>Vyberte podkategorii</option>');

                    subcategories.forEach(function(sub) {
                        newSelect.append(`<option value="${sub.id}">${sub.name}</option>`);
                    });

                    // Přidání nového selectu do kontejneru
                    container.append(newSelect);
                }
            },
            error: function() {
                console.error('Chyba při načítání podkategorií.');
            }
        });
    }

    // Delegace události pro dynamicky přidané selecty
    $('#subcategory-container').on('change', '.category-select', function() {
        // Odstranění všech následujících selectů
        $(this).nextAll('.category-select').remove();

        const selectedId = $(this).val();
        if (selectedId) {
            loadSubcategories(selectedId, $('#subcategory-container'));
        }
    });

    // Událost při změně hlavní kategorie
    $('.category-select').first().on('change', function() {
        // Odstranění všech podkategorií
        $('#subcategory-container').empty();

        const selectedId = $(this).val();
        if (selectedId) {
            loadSubcategories(selectedId, $('#subcategory-container'));
        }
    });
});