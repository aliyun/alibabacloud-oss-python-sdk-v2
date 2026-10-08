import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess

parser = argparse.ArgumentParser(description="put data pipeline configuration sample")
parser.add_argument('--region', help='The region of the bucket.', required=True)
parser.add_argument('--endpoint', help='The endpoint of OSS.')
parser.add_argument('--data-pipeline-name', help='The name of the data pipeline.', required=True)
parser.add_argument('--bucket', help='The input bucket name.', required=True)
parser.add_argument('--role', help='The role for the data pipeline.')
parser.add_argument('--description', help='The description of the data pipeline.')

def main():
    args = parser.parse_args()
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint
    client = oss_dataprocess.Client(cfg)

    configuration = oss_dataprocess.models.PutDataPipelineConfigurationConfiguration(
        data_pipeline_description=args.description,
        sources=[oss_dataprocess.models.DataPipelineSource(
            input_bucket=args.bucket,
            input_data_scope='All',
        )],
    )

    # To create a V2 data pipeline, comment the configuration above and uncomment this block.
    # The vector buckets and indexes must already exist and match the required dimensions.
    # configuration = oss_dataprocess.models.PutDataPipelineConfigurationConfiguration(
    #     data_pipeline_description=args.description,
    #     sources=[oss_dataprocess.models.DataPipelineSource(
    #         input_bucket=args.bucket,
    #         input_data_scope='All',
    #         ignore_delete=False,
    #         filter_configuration=oss_dataprocess.models.DataPipelineSourceFilterConfiguration(
    #             object_media_types=['image', 'video', 'text'],
    #         ),
    #     )],
    #     model_tier='standard',
    #     data_pipeline_data_process_configuration=oss_dataprocess.models.DataPipelineDataProcessConfiguration(
    #         search_mode='balanced',
    #         insights=oss_dataprocess.models.DataPipelineInsights(
    #             image=oss_dataprocess.models.InsightsImage(
    #                 caption=oss_dataprocess.models.InsightsCaption(
    #                     prompt='Describe the image.'),
    #             ),
    #             video=oss_dataprocess.models.InsightsVideo(
    #                 caption=oss_dataprocess.models.InsightsCaption(
    #                     prompt='Describe each video scene.'),
    #                 frame_embedding=oss_dataprocess.models.InsightsFrameEmbedding(
    #                     snapshot=oss_dataprocess.models.InsightsSnapshot(
    #                         mode='interval', interval=1.0),
    #                 ),
    #             ),
    #         ),
    #     ),
    #     destination=oss_dataprocess.models.DataPipelineDestination(
    #         image_embedding=oss_dataprocess.models.ImageEmbedding(
    #             bucket='vector-bucket', index_name='image', prefix='v2'),
    #         image_text_embedding=oss_dataprocess.models.ImageTextEmbedding(
    #             bucket='vector-bucket', index_name='image-text', prefix='v2'),
    #         video_frame_embedding=oss_dataprocess.models.VideoFrameEmbedding(
    #             bucket='vector-bucket', index_name='video-frame', prefix='v2'),
    #         video_text_embedding=oss_dataprocess.models.VideoTextEmbedding(
    #             bucket='vector-bucket', index_name='video-text', prefix='v2'),
    #         document_chunk_embedding=oss_dataprocess.models.DocumentChunkEmbedding(
    #             bucket='vector-bucket', index_name='document', prefix='v2'),
    #     ),
    # )

    result = client.put_data_pipeline_configuration(oss_dataprocess.models.PutDataPipelineConfigurationRequest(
        data_pipeline_name=args.data_pipeline_name,
        role=args.role,
        configuration=configuration,
    ))
    print(f'status code: {result.status_code}, request id: {result.request_id}')

if __name__ == "__main__":
    main()
