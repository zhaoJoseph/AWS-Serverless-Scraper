import postgres from 'postgres';
import pg from 'pg'
import dotenv from 'dotenv'
import BaseError from '../../utils/baseError.js';
import format from 'pg-format'
import error from '../../utils/error.js'
import Logger from '../../utils/logger.js';

dotenv.config()

const { PGHOST, PGDATABASE, PGUSER, PGPASSWORD, ENDPOINT_ID } = process.env;
const URL = `postgres://${PGUSER}:${PGPASSWORD}@${PGHOST}/${PGDATABASE}?sslmode=require&ptions=project%3D${ENDPOINT_ID}`;

const sql = postgres(URL, { ssl: 'require' });

const funcs = {

getPostgresVersion: async () => {
  const result = await sql`select version()`;
  console.log(result);
},

aggregateData: async (list) => {
  try{
    const Client = pg.Client
    const dataList = await JSON.stringify(list)
    const client = new Client({
      connectionString: URL
    });
    await client.connect();
    const query = format("INSERT INTO deals_table (title, url, time_inserted) SELECT * FROM json_populate_recordset((null, null, current_timestamp)::deals_table, %L) ON CONFLICT DO NOTHING;", dataList)
    const res = await client.query(query);
    Logger.info(res)
    await client.end();

  } catch (err) {
    Logger.error(err)

    if(!err.code) {
      throw new BaseError(err.error, err.codes.SERVER_ERROR, err.error)
    }else {
      throw new BaseError(err.name, err.code, err.message + ' ' + err.detail)
    }
  } 
},

removeExpired: async () => {
  try{
    const Client = pg.Client
    const client = new Client({
      connectionString: URL
    });
    await client.connect();
    const query = format("CALL remove_expired();");
    const res = await client.query(query);
    Logger.info(res)
    await client.end();

  } catch (err) {
    Logger.error(err)

    if(!err.code) {
      throw new BaseError(err.error, err.codes.SERVER_ERROR, err.error)
    }else {
      throw new BaseError(err.name, err.code, err.message + ' ' + err.detail)
    }
  } 
}

}

export default funcs