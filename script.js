// Fetch exam data from the backend API
fetch('http://localhost:8080/api/exams')  // Fetch data from the API, not from a JSON file
    .then(response => response.json())
    .then(data => {
        let examList = document.getElementById('exam-list');

        data.forEach(exam => {
            let examItem = document.createElement('div');
            let examName = document.createElement('h2');
            examName.innerText = exam.exam_name;
            examItem.classList.add('exam-item');

            let examLink = document.createElement('button');
            examLink.textContent = "Apply Now";
            examLink.classList.add('button');
            examLink.addEventListener('click', () => {
                window.location.href = exam.link;  // Redirect to the exam link
            });

            examItem.appendChild(examName);
            examItem.appendChild(examLink);
            examList.appendChild(examItem);
        });
    })
    .catch(error => {
        console.error('Error fetching exam data:', error);
    });
