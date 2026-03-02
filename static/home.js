document.addEventListener("DOMContentLoaded", async () => {
  const loadBlobs = async () => {
  try {
    const response = await fetch("/api/blobs");
    const data = await response.json();
    const blobList = document.getElementById("blob-table-body");

    if (data.status === "success") {
      data.data.forEach(blob => {
        const listItem = document.createElement("tr");
        listItem.innerHTML = `
          <td>${blob.name}</td>
          <td>${blob.size}</td>
          <td>${blob.lastModified}</td>
          <td>
            <button class="btn-download" data-name="${blob.name}">Download</button>
            <button class="btn-delete" data-name="${blob.name}">Delete</button>
          </td>
        `;

        const deleteButton = listItem.querySelector(".btn-delete");
        deleteButton.addEventListener("click", async () => {
          if (confirm(`Are you sure you want to delete '${blob.name}'?`)) {
            try {
              const response = await fetch(`/api/blob/${blob.name}/delete`, {
                method: "DELETE"
              });

              if (response.ok) {
                window.location.reload();
              } else {
                alert("Failed to delete blob.");
              }
            } catch (error) {
              console.error("Error deleting blob:", error);
              alert("An error occurred while deleting the blob.");
            }
          }
        });

        const downloadButton = listItem.querySelector(".btn-download");
        downloadButton.addEventListener("click", async () => {
          try {
            const response = await fetch(`/api/blob/${blob.name}/download`);
            if (response.ok) {
              const blobData = await response.blob();
              const url = window.URL.createObjectURL(blobData);
              const a = document.createElement("a");
              a.href = url;
              a.download = blob.name;
              document.body.appendChild(a);
              a.click();
              window.URL.revokeObjectURL(url);
            } else {
              alert("Failed to download blob.");
            }
          } catch (error) {
            console.error("Error downloading blob:", error);
            alert("An error occurred while downloading the blob.");
          }
        });

        blobList.appendChild(listItem);
      });
    } else {
      blobList.textContent = "Failed to load blobs.";
    }
  } catch (error) {
    console.error("Error loading blobs:", error);
  }
};

  loadBlobs();

  const initializeForm = () => {
    const uploadButton = document.getElementById("btn-upload");
    uploadButton.addEventListener("click", async (e) => {
      e.preventDefault();
      const fileInput = document.getElementById("input-file");
      const file = fileInput.files[0];
      if (!file) {
        alert("Please select a file to upload.");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("/api/blobs/upload", {
          method: "POST",
          body: formData
        });

        if (response.ok) {
          window.location.reload();
          return;
        } else {
          alert("Failed to upload blob.");
        }
      } catch (error) {
        console.error("Error uploading blob:", error);
        alert("An error occurred while uploading the blob.");
      }
    });
  };

  initializeForm();
});