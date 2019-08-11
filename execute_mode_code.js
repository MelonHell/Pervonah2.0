var status;
var comment_id;

var post = API.newsfeed.get({'filters': 'post', 'count': 1, 'source_ids': ''})['items'][0];
if (post['date'] > last_post_date) {
    status = true;
    comment_id = API.wall.createComment({'owner_id': post['source_id'], 'post_id': post['post_id'], 'message': comment_text})['comment_id'];
} else {
    status = false;
    comment_id = null;
};
return {'status': status, 'comment_id': comment_id, 'post_id': post['post_id'], 'source_id': post['source_id'], 'date': post['date']};