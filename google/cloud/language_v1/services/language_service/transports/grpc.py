# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.language_v1.types import language_service

from .base import LanguageServiceTransport, DEFAULT_CLIENT_INFO


class LanguageServiceGrpcTransport(LanguageServiceTransport):
    """gRPC backend transport for LanguageService.

    Provides text analysis operations such as sentiment analysis
    and entity recognition.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "language.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "language.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def analyze_sentiment(
        self,
    ) -> Callable[
        [language_service.AnalyzeSentimentRequest],
        language_service.AnalyzeSentimentResponse,
    ]:
        r"""Return a callable for the analyze sentiment method over gRPC.

        Analyzes the sentiment of the provided text.

        Returns:
            Callable[[~.AnalyzeSentimentRequest],
                    ~.AnalyzeSentimentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_sentiment" not in self._stubs:
            self._stubs["analyze_sentiment"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnalyzeSentiment",
                request_serializer=language_service.AnalyzeSentimentRequest.serialize,
                response_deserializer=language_service.AnalyzeSentimentResponse.deserialize,
            )
        return self._stubs["analyze_sentiment"]

    @property
    def analyze_entities(
        self,
    ) -> Callable[
        [language_service.AnalyzeEntitiesRequest],
        language_service.AnalyzeEntitiesResponse,
    ]:
        r"""Return a callable for the analyze entities method over gRPC.

        Finds named entities (currently proper names and
        common nouns) in the text along with entity types,
        salience, mentions for each entity, and other
        properties.

        Returns:
            Callable[[~.AnalyzeEntitiesRequest],
                    ~.AnalyzeEntitiesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_entities" not in self._stubs:
            self._stubs["analyze_entities"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnalyzeEntities",
                request_serializer=language_service.AnalyzeEntitiesRequest.serialize,
                response_deserializer=language_service.AnalyzeEntitiesResponse.deserialize,
            )
        return self._stubs["analyze_entities"]

    @property
    def analyze_entity_sentiment(
        self,
    ) -> Callable[
        [language_service.AnalyzeEntitySentimentRequest],
        language_service.AnalyzeEntitySentimentResponse,
    ]:
        r"""Return a callable for the analyze entity sentiment method over gRPC.

        Finds entities, similar to
        [AnalyzeEntities][google.cloud.language.v1.LanguageService.AnalyzeEntities]
        in the text and analyzes sentiment associated with each entity
        and its mentions.

        Returns:
            Callable[[~.AnalyzeEntitySentimentRequest],
                    ~.AnalyzeEntitySentimentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_entity_sentiment" not in self._stubs:
            self._stubs["analyze_entity_sentiment"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnalyzeEntitySentiment",
                request_serializer=language_service.AnalyzeEntitySentimentRequest.serialize,
                response_deserializer=language_service.AnalyzeEntitySentimentResponse.deserialize,
            )
        return self._stubs["analyze_entity_sentiment"]

    @property
    def analyze_syntax(
        self,
    ) -> Callable[
        [language_service.AnalyzeSyntaxRequest], language_service.AnalyzeSyntaxResponse
    ]:
        r"""Return a callable for the analyze syntax method over gRPC.

        Analyzes the syntax of the text and provides sentence
        boundaries and tokenization along with part of speech
        tags, dependency trees, and other properties.

        Returns:
            Callable[[~.AnalyzeSyntaxRequest],
                    ~.AnalyzeSyntaxResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "analyze_syntax" not in self._stubs:
            self._stubs["analyze_syntax"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnalyzeSyntax",
                request_serializer=language_service.AnalyzeSyntaxRequest.serialize,
                response_deserializer=language_service.AnalyzeSyntaxResponse.deserialize,
            )
        return self._stubs["analyze_syntax"]

    @property
    def classify_text(
        self,
    ) -> Callable[
        [language_service.ClassifyTextRequest], language_service.ClassifyTextResponse
    ]:
        r"""Return a callable for the classify text method over gRPC.

        Classifies a document into categories.

        Returns:
            Callable[[~.ClassifyTextRequest],
                    ~.ClassifyTextResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "classify_text" not in self._stubs:
            self._stubs["classify_text"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/ClassifyText",
                request_serializer=language_service.ClassifyTextRequest.serialize,
                response_deserializer=language_service.ClassifyTextResponse.deserialize,
            )
        return self._stubs["classify_text"]

    @property
    def annotate_text(
        self,
    ) -> Callable[
        [language_service.AnnotateTextRequest], language_service.AnnotateTextResponse
    ]:
        r"""Return a callable for the annotate text method over gRPC.

        A convenience method that provides all the features
        that analyzeSentiment, analyzeEntities, and
        analyzeSyntax provide in one call.

        Returns:
            Callable[[~.AnnotateTextRequest],
                    ~.AnnotateTextResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "annotate_text" not in self._stubs:
            self._stubs["annotate_text"] = self.grpc_channel.unary_unary(
                "/google.cloud.language.v1.LanguageService/AnnotateText",
                request_serializer=language_service.AnnotateTextRequest.serialize,
                response_deserializer=language_service.AnnotateTextResponse.deserialize,
            )
        return self._stubs["annotate_text"]


__all__ = ("LanguageServiceGrpcTransport",)
