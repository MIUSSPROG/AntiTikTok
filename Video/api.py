import shutil
from typing import List
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from starlette.requests import Request
from starlette.responses import StreamingResponse, HTMLResponse
from starlette.templating import Jinja2Templates

# from models import Video, User
from Video.models import User, Video
from Video.schemas import UploadVideo, GetVideo, Message, GetListVideo
from Video.services import write_video, save_video, open_file

video_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@video_router.post("/")
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...)
):
    user = await User.objects.first()
    return await save_video(user, file, title, description, background_tasks)
    # file_name = f'media/{file.filename}'


# @video_router.post("/img")
# async def upload_image(files: List[UploadFile] = File(...)):
#     for img in files:
#         with open(f'{img.filename}', 'wb') as buffer:
#             shutil.copyfileobj(img.file, buffer)
#
#     return {"file_name": "Good"}


# @video_router.post("/info")
# async def info_set(info: UploadVideo):
#     return info


# @video_router.post("/video")
# async def create_video(video: Video):
#     await video.save()
#     return video


# @video_router.get("/video/{video_pk}", response_model=GetVideo, responses={404: {"model": Message}})
# async def get_video(video_pk: int):
#     file = await Video.objects.select_related('user').get(pk=video_pk)
#     file_like = open(file.dict().get('file'), mode="rb")
#     return StreamingResponse(file_like, media_type="video/mp4")


@video_router.get("/user/{user_pk}", response_model=List[GetListVideo])
async def get_list_video(user_pk: int):
    video_list = await Video.objects.filter(user=user_pk).all()
    return video_list

    # # user = {'id': 25, 'name': 'Pipec'}
    # # video = {'title': 'Test', 'description': 'Description'}
    # user = User(id=25, name='Pipec')
    # video = UploadVideo(title='Test', description='Description')
    # info = GetVideo(user=user, video=video)
    # # return info
    # return JSONResponse(status_code=200, content=info.dict())


@video_router.get("/index/{video_pk}", response_class=HTMLResponse)
async def get_video(request: Request, video_pk: int):
    return templates.TemplateResponse("index.html", {"request": request, "path": video_pk})


@video_router.get("/video/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers
    })
    return response
# async def fake_video_streamer():
#     for i in range(10):
#         yield b"some fake video bytes"
#
#
# @video_router.get("/fake")
# async def main():
#     return StreamingResponse(fake_video_streamer())
