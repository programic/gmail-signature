function exportUsersToJSON() {
  // Fetch all users in the domain
  let users = AdminDirectory.Users.list({
    domain: 'example.com', // Replace with your actual domain
    customer: 'my_customer'
  }).users;

// Specify the target OU
  let targetOU = 'Your OU'; // Replace with the actual OU name

  // Prepare an array to store user data
  let userData = [];


  // Extract relevant information for each user, filtering by OU
  users.forEach(user => {
    if (user.orgUnitPath === '/' + targetOU) { // Check if the user belongs to the target OU
      let phone = user.phones ? user.phones[0].value : 'FALLBACK PHONE NUMBER'; // Use user's phone number or default
      userData.push({
        username: user.primaryEmail,
        full_name: user.name.fullName,
        email: user.primaryEmail,
        job_title: user.organizations ? user.organizations[0].title : '', // Extract job title
        phone: phone
      });
    }
  });
  // Convert user data to JSON string
  let jsonData = JSON.stringify(userData, null, 2); // 2 spaces for indentation

  // Create a blob for the JSON data
  let blob = Utilities.newBlob(jsonData, 'application/json', 'users.json');

  // Download the JSON file
  DriveApp.createFile(blob); // Save to Google Drive first
  // You'll need to manually download the 'users.json' file from your Google Drive
}