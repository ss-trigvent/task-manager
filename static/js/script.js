$(document).ready(function() {
    fetchTasks();

    function fetchTasks() {
        $.ajax({
            url: '/tasks/',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                if (response.statusCode == 200){
                    displayTasks(response.data);
                }
            },
            error: function(xhr, status, error) {
                console.error("Failed to fetch tasks: ", error);
            }
        });
    }

    function displayTasks(tasks) {
        $('#todo-tasks').empty();
        $('#inprogress-tasks').empty();
        $('#done-tasks').empty();
        tasks.forEach(function(task) {
            let taskHtml = `
                <div class="task-item" id="task-${task.id}">
                    <h3>${task.title}</h3>
                    <p>${task.description}</p>
                    <p class="due-date">Due: ${task.due_date}</p>
                </div>
            `;

            if (task.status === 'Todo') {
                $('#todo-tasks').append(taskHtml);
            } else if (task.status === 'Inprogress') {
                $('#inprogress-tasks').append(taskHtml);
            } else if (task.status === 'Complete') {
                $('#done-tasks').append(taskHtml);
            }
        });
    }

});


$(document).on('click', '.task-item', function() {
    let taskId = $(this).attr('id').split('-')[1];

    $.ajax({
        url: `/tasks/${taskId}/`,
        type: 'GET',
        success: function(response) {
            $('#taskId').val(response.id);
            $('#taskTitle').text(response.title);
            $('#taskDescription').text(response.description);
            $('#taskDueDate').text(response.due_date);
            $('#taskStatus').text(response.status);
            $('#taskCreatedAt').text(response.created_at);
            $('#taskCreatedBy').text(response.created_by.username);
            $('#taskUpdatedAt').text(response.updated_at);

            var userSelect = $('#userList');
            userSelect.empty();
            userSelect.append('<option value="">Select User</option>');
            $.each(response.all_users, function(index, user) {
                userSelect.append(`<option value="${user.id}">${user.username}</option>`);
            });

           get_members_list(taskId)

            $.ajax({
                url: `/tasks/${taskId}/comments/`,
                type: 'GET',
                success: function(commentsResponse) {
                    $('#taskComments').empty();
                    commentsResponse.data.forEach(function(comment) {
                        $('#taskComments').append(`<li class="comment"><strong>${comment.username}:</strong> ${comment.comment} <br><small>${comment.created_at}</small></li>`);
                        });
                },
                error: function(xhr, status, error) {
                    console.error("Failed to fetch task comments: ", error);
                }
            });

            $('#taskDetailsModal').css('display', 'block');
        },
        error: function(xhr, status, error) {
            console.error("Failed to fetch task details: ", error);
        }
    });
});

$('.close-btn').click(function() {
    $('#taskDetailsModal').css('display', 'none');
});

$(window).click(function(event) {
    if (event.target == document.getElementById('taskDetailsModal')) {
        $('#taskDetailsModal').css('display', 'none');
    }
    else if(event.target == document.getElementById('userListModal')) {
        $('#userListModal').hide();
    }
});


$(document).on('click', '.btn-remove-member', function() {
    event.preventDefault();

    const memberId = event.target.dataset.memberId;
    const taskId = event.target.dataset.taskId;
    const memberItem = $(this).closest('.member');
    
    const confirmed = confirm("Are you sure you want to remove this user?");
    if (confirmed) {
        $.ajax({
            url: `/tasks/${taskId}/members/remove/`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                member_id: memberId 
            }),
            success: function(response) {
                memberItem.remove();
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }
});



$('#btnAddMember').click(function() {
    $('#userListModal').show();
});


$('#confirmAddUserBtn').on('click', function() {
    var selectedUserId = $('#userList').val();
    var taskId = $('#taskId').val();

    if (selectedUserId) {
        var username = $('#userSelect option:selected').text();

        if (confirm(`Are you sure you want to add ${username} as a member?`)) {
            $.ajax({
                url: `/tasks/${taskId}/members/add/`,
                method: 'POST',
                data: JSON.stringify({
                    member_id: selectedUserId
                }),
                contentType: 'application/json',
                success: function(response) {
                    if (response.status === 'success') {
                        get_members_list(taskId)
                    } else {
                        alert('Failed to add member.');
                    }
                },
                error: function() {
                    alert('An error occurred.');
                }
            });
        }
    } else {
        alert('Please select a user.');
    }
    $('#userListModal').hide();

});


function get_members_list(taskId){
    $.ajax({
        url: `/tasks/${taskId}/members/`,
        type: 'GET',
        success: function(membersResponse) {
            $('#taskMembers').empty();
            membersResponse.data.forEach(function(member) {
                
            $('#taskMembers').append(`<li class="member">
                <span class="name">${member.username}</span> 
                <span class="email">${member.email}</span>
                <button class="btn-remove-member" data-member-id="${member.userid}" data-task-id="${taskId}">Remove</button>
                </li>`);
            });
        },
        error: function(xhr, status, error) {
            console.error("Failed to fetch task members: ", error);
        }
    });
}


function openStatusDropdown() {
    document.getElementById('statusDropdown').style.display = 'block';
}


function updateTaskStatus(status) {
    var taskId = document.getElementById('taskId').value;
    $.ajax({
        url: `/tasks/update/${taskId}/`,
        method: 'PATCH',
        contentType: 'application/json',
        data: JSON.stringify({ status: status }),
        success: function(response) {
            if (response.status === 'success') {
                document.getElementById('taskStatus').innerText = status;
                document.getElementById('statusDropdown').style.display = 'none';
                window.location.href = '/';
            } else {
                alert('Error updating status');
            }
        },
        error: function() {
            alert('Error updating status');
        }
    });
}



$('#btnAddComment').click(function() {
    var commentText = $('#newComment').val();
    var loggedInUserName = $('#loggedInUserName').val();
    var taskId = $('#taskId').val();
    
    if (commentText.trim() === '') {
        alert('Comment cannot be empty.');
        return;
    }

    $.ajax({
        url: `/tasks/${taskId}/comments/add/`,
        type: 'POST',
        data: {
            comment: commentText,
            username: loggedInUserName
        },
        success: function(response) {
            $('#taskComments').append(
                `<li class="comment"><strong> ${loggedInUserName} :</strong> 
                ${commentText} <br><small> ${new Date().toISOString()} </small></li>`
            );
            $('#newComment').val('');
        },
        error: function(error) {
            alert('Error adding comment. Please try again.');
        }
    });
});


$('#btnDeleteTask').click(function() {
    var taskId = $('#taskId').val();
    
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    $.ajax({
        url: `/tasks/delete/${taskId}/`,
        type: 'DELETE',
        success: function(response) {
            window.location.href = '/';
        },
        error: function(error) {
            alert('Error deleting task. Please try again.');
        }
    });
});


function makeTitleEditable() {
    var titleElem = document.getElementById('taskTitle');
    var inputElem = document.getElementById('editTitleInput');
    var btnElem = document.getElementById('btnUpdateTitle');
    
    inputElem.value = titleElem.innerText;
    inputElem.style.display = 'inline';
    btnElem.style.display = 'inline';
    inputElem.focus();
    titleElem.style.display = 'none';
}

function updateTaskTitle() {
    var taskId = document.getElementById('taskId').value;
    var inputElem = document.getElementById('editTitleInput');
    var newTitle = inputElem.value;
    
    $.ajax({
        url: `/tasks/update/${taskId}/`,
        method: 'PATCH',
        contentType: 'application/json',
        data: JSON.stringify({ title: newTitle }),
        success: function(response) {
            if (response.status === 'success') {
                document.getElementById('taskTitle').innerText = newTitle;
                document.getElementById('taskTitle').style.display = 'block';
                inputElem.style.display = 'none';
                document.getElementById('btnUpdateTitle').style.display = 'none';
            } else {
                alert('Error updating title');
            }
        },
        error: function() {
            alert('Error updating title');
        }
    });
}


function makeDescriptionEditable() {
    var descriptionElem = document.getElementById('taskDescription');
    var inputElem = document.getElementById('editDescriptionInput');
    var btnElem = document.getElementById('btnUpdateDescription');
    
    inputElem.value = descriptionElem.innerText;
    inputElem.style.display = 'block';
    btnElem.style.display = 'block';
    inputElem.focus();
    descriptionElem.style.display = 'none';
}

function updateTaskDescription() {
    var taskId = document.getElementById('taskId').value;
    var inputElem = document.getElementById('editDescriptionInput');
    var newDescription = inputElem.value;
    
    $.ajax({
        url: `/tasks/update/${taskId}/`,
        method: 'PATCH',
        contentType: 'application/json',
        data: JSON.stringify({ description: newDescription }),
        success: function(response) {
            if (response.status === 'success') {
                document.getElementById('taskDescription').innerText = newDescription;
                document.getElementById('taskDescription').style.display = 'block';
                inputElem.style.display = 'none';
                document.getElementById('btnUpdateDescription').style.display = 'none';
            } else {
                alert('Error updating description');
            }
        },
        error: function() {
            alert('Error updating description');
        }
    });
}

function openAddTaskModal() {
    $('#addTaskModal').show();
}

$('.close-btn').on('click', function () {
    $('.modal').hide();
});

$('#saveTaskBtn').on('click', function (e) {
    e.preventDefault();
    let title = $('#taskTitleInput').val();
    let description = $('#taskDescriptionInput').val();
    let due_date = $('#taskDueDateInput').val();
    let status = $('#taskStatusInput').val();

    $.ajax({
        url: '/tasks/create/',
        method: 'POST',
        data: {
            title: title,
            description: description,
            due_date: due_date,
            status: status,
        },
        success: function (data) {
            window.location.href = '/';
        },
        error: function (error) {
            console.error("Error adding task:", error);
        }
    });
});
