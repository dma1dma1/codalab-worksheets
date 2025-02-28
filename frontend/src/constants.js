// Should match codalab/common.py#CODALAB_VERSION
export const CODALAB_VERSION = '1.7.0';

// Name Regex to match the backend in spec_utils.py
export const NAME_REGEX = /^[a-zA-Z_][a-zA-Z0-9_.-]*$/i;

export const NAVBAR_HEIGHT = 58;
export const HEADER_HEIGHT = 170;
export const WORKSHEET_HEADER_HEIGHT = 78;
export const FOOTER_HEIGHT = 25;

// Worksheet width
export const EXPANDED_WORKSHEET_WIDTH = '100%';
export const NARROW_WORKSHEET_WIDTH = '65%';
export const FILE_SIZE_LIMIT_GB = 2;
export const FILE_SIZE_LIMIT_B = FILE_SIZE_LIMIT_GB * 1024 * 1024 * 1024;
export const LOCAL_STORAGE_WORKSHEET_WIDTH = 'newWorksheetWidth';

// Dialog constants
export const DIALOG_TYPES = {
    OPEN_DELETE_BUNDLE: 'delete_bundle',
    OPEN_KILL: 'kill_bundle',
    OPEN_DELETE_MARKDOWN: 'delete_markdown_block',
    OPEN_DELETE_WORKSHEET: 'delete_whole_worksheet',
    OPEN_ERROR_DIALOG: 'error_dialog',
    OPEN_DELETE_SCHEMA: 'delete_schema',
    OPEN_CREATE_CONTENT: 'create_content_block',
};

// Bundle fetch status values; corresponds with FetchStatusCodes in backend
export const FETCH_STATUS_SCHEMA = {
    UNKNOWN: 'unknown',
    PENDING: 'pending',
    BRIEFLY_LOADED: 'briefly_loaded',
    READY: 'ready',
    NOT_FOUND: 'not_found',
    NO_PERMISSION: 'no_permission',
};

// Default Duration for messagePopover shown on the worksheet
export const AUTO_HIDDEN_DURATION = 1500;

// All possible bundle states
export const BUNDLE_STATES: String[] = [
    'uploading',
    'created',
    'staged',
    'making',
    'starting',
    'preparing',
    'running',
    'finalizing',
    'ready',
    'failed',
    'killed',
    'worker_offline',
];

// All possible final bundle states
export const FINAL_BUNDLE_STATES = ['ready', 'failed', 'killed'];

export const RUN_BUNDLE_STATES = [
    'created',
    'staged',
    'starting',
    'preparing',
    'running',
    'finalizing',
    'ready',
];

export const UPLOADED_BUNDLE_STATES = ['created', 'uploading', 'ready'];

export const MAKE_BUNDLE_STATES = ['created', 'making', 'ready'];

export const OFFLINE_STATE = 'worker_offline';

// Autofill types for schemas.
export const DEFAULT_POST_PROCESSOR = {
    time: 'duration',
    size: 'size',
    date: 'date',
};

// The rows should be synced with https://github.com/codalab/codalab-worksheets/blob/master/codalab/lib/worksheet_util.py#L575
export const DEFAULT_SCHEMA_ROWS = [
    {
        field: 'uuid',
        'generalized-path': 'uuid',
        'post-processor': '[0:8]',
        from_schema_name: '',
    },
    {
        field: 'name',
        'generalized-path': 'name',
        from_schema_name: '',
    },
    {
        field: 'summary[0:1024]',
        'generalized-path': 'summary',
        'post-processor': '[0:1024]',
        from_schema_name: '',
    },
    {
        field: 'data_size',
        'generalized-path': 'data_size',
        from_schema_name: '',
    },
    {
        field: 'state',
        'generalized-path': 'state',
        from_schema_name: '',
    },
    {
        field: 'description',
        'generalized-path': 'description',
        from_schema_name: '',
    },
];

// Documentation URLs (object structure matches mkdocs.yml)
export const DOCS = {
    concepts: {
        bundleLifecycle: 'https://codalab-worksheets.readthedocs.io/en/latest/Bundle-Lifecycle',
    },
};
