const getId = (url) => {
    const Url = new URL(url);
    return Url.searchParams.get('id'); 
}


const postData = (url, options) => {
	return fetch(
		'http://localhost:8000' + url,
		{
            "headers": {
                "Content-Type": "application/json",
            },
            "method": "post",
		    "body": JSON.stringify(options)
		},
	)
}


const deleteData = (url, options) => {
	return fetch(
		'http://localhost:8000' + url,
		{
            "headers": {
                "Content-Type": "application/json",
            },
            "method": "delete",
		    "body": JSON.stringify(options)
		},
	)
}