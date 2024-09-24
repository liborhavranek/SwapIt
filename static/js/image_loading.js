document.addEventListener('DOMContentLoaded', function () {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('images');
    const previewContainer = document.getElementById('preview-container');

    // Funkce pro přidání obrázku do náhledu
    function addImage(file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const col = document.createElement('div');
            col.classList.add('col-lg-4', 'col-md-6', 'col-12', 'preview-image');


            const img = document.createElement('img');
            img.src = e.target.result;
            img.alt = file.name;

            const removeBtn = document.createElement('button');
            removeBtn.classList.add('remove-image');
            removeBtn.innerHTML = '&times;';
            removeBtn.setAttribute('aria-label', 'Odstranit obrázek');
            removeBtn.onclick = function () {
                previewContainer.removeChild(col);
            };

            col.appendChild(img);
            col.appendChild(removeBtn);
            previewContainer.appendChild(col);
        };
        reader.readAsDataURL(file);
    }

    // Při změně souboru
    fileInput.addEventListener('change', function () {
        const files = this.files;
        for (let file of files) {
            if (file.type.startsWith('image/')) {
                addImage(file);
            }
        }
    });

    // Při přetažení souborů
    uploadArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function (e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragover');

        const files = e.dataTransfer.files;
        for (let file of files) {
            if (file.type.startsWith('image/')) {
                addImage(file);
            }
        }
    });

    // Kliknutí na upload area aktivuje file input
    uploadArea.addEventListener('click', function () {
        fileInput.click();
    });
});